#!/usr/bin/env python3
"""
异常检查脚本
检查华为云中的异常操作记录
"""

import json
import subprocess
import sys
from typing import List, Dict, Any, Optional, Union

import hmac
import hashlib
import urllib.request
from urllib.parse import quote
from datetime import datetime, timezone

def run_hcloud(service: str, operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """执行 hcloud 命令并返回 JSON 结果"""
    cmd = ["hcloud", service, operation]

    for key, value in args.items():
        if value is not None:
            cmd.append(f"--{key}={value}")

    cmd.extend(["--cli-output=json"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        if result.returncode != 0:
            return {"error": result.stderr, "returncode": result.returncode}

        # 尝试解析JSON
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            # JSON解析失败，返回原始输出
            return {
                "error": f"JSON解析失败，可能是CTS服务未启用或数据格式问题",
                "raw_output": result.stdout[:500],  # 只保留前500字符
                "json_error": str(e)
            }
    except subprocess.TimeoutExpired:
        return {"error": "命令执行超时"}
    except Exception as e:
        return {"error": f"执行失败: {str(e)}"}



def query_traces(region: str, project_id: str, trace_rating: Optional[str] = None, 
                 from_time: Optional[int] = None, to_time: Optional[int] = None, limit: int = 200) -> Dict[str, Any]:
    """查询追踪记录"""
    args: Dict[str, Union[str, int]] = {
        "cli-region": region,
        "project_id": project_id,
        "trace_type": "system",
        "limit": limit
    }
    if trace_rating:
        args["trace_rating"] = trace_rating
    # 不传时间参数，让API返回最近的记录

    return run_hcloud("CTS", "ListTraces", args)

def analyze_traces(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    """分析追踪记录"""
    analysis: Dict[str, Any] = {
        "total": len(traces),
        "by_rating": {"normal": 0, "warning": 0, "incident": 0},
        "by_service": {},
        "by_user": {},
        "failed_operations": [],
        "sensitive_operations": [],
        "delete_operations": []
    }

    # 敏感操作关键词
    sensitive_keywords = [
        "delete", "remove", "terminate", "destroy",
        "attach", "detach", "authorize", "revoke",
        "createAccessKey", "deleteAccessKey",
        "createUser", "deleteUser", "updateUser",
        "createSecurityGroupRule", "deleteSecurityGroupRule",
        "createRole", "deleteRole", "attachRole"
    ]

    delete_keywords = ["delete", "remove", "terminate", "destroy"]

    for trace in traces:
        # 按级别统计
        rating = trace.get("trace_rating", "normal")
        analysis["by_rating"][rating] = analysis["by_rating"].get(rating, 0) + 1

        # 按服务统计
        service = trace.get("service_type", "unknown")
        analysis["by_service"][service] = analysis["by_service"].get(service, 0) + 1

        # 按用户统计
        user_info = trace.get("user", {})
        if isinstance(user_info, dict):
            user = user_info.get("name", "unknown")
        else:
            user = str(user_info)
        analysis["by_user"][user] = analysis["by_user"].get(user, 0) + 1

        # 检查失败操作
        code = trace.get("code", "200")
        try:
            code_int = int(code)
            if code_int < 200 or code_int >= 300:
                analysis["failed_operations"].append({
                    "time": trace.get("time"),
                    "user": trace.get("user", {}).get("name", "unknown") if isinstance(trace.get("user"), dict) else str(trace.get("user")),
                    "operation": trace.get("trace_name"),
                    "code": code_int,
                    "resource": trace.get("resource_name")
                })
        except (ValueError, TypeError):
            pass

        # 检查敏感操作
        trace_name = trace.get("trace_name", "").lower()
        if any(keyword.lower() in trace_name for keyword in sensitive_keywords):
            analysis["sensitive_operations"].append({
                "time": trace.get("time"),
                "user": trace.get("user"),
                "operation": trace.get("trace_name"),
                "resource": trace.get("resource_name"),
                "rating": rating
            })

        # 检查删除操作
        if any(keyword in trace_name for keyword in delete_keywords):
            analysis["delete_operations"].append({
                "time": trace.get("time"),
                "user": trace.get("user"),
                "operation": trace.get("trace_name"),
                "resource": trace.get("resource_name"),
                "rating": rating
            })

    return analysis

def generate_user_friendly_message(trace: Dict[str, Any]) -> Dict[str, Any]:
    """生成用户友好的错误说明"""
    code = trace.get("code", "200")
    try:
        code_int = int(code)
    except (ValueError, TypeError):
        code_int = 200

    operation = trace.get("trace_name", "")
    resource = trace.get("resource_name", "未指定")
    user_info: Union[str, Dict[str, str]] = trace.get("user", {})
    if isinstance(user_info, dict):
        user = user_info.get("name", "未知用户")
    else:
        user = str(user_info)

    # 转换时间戳
    time_stamp = trace.get("time")
    if time_stamp:
        try:
            time_str = datetime.fromtimestamp(time_stamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            time_str = str(time_stamp)
    else:
        time_str = "未知时间"

    # 错误码转换
    error_messages = {
        400: "请求参数错误",
        401: "身份验证失败，请检查访问密钥是否正确或是否已过期",
        403: "权限不足，您没有执行此操作的权限",
        404: "资源不存在，该资源可能已被删除或ID错误",
        409: "资源状态冲突，该资源正在被其他操作使用",
        500: "系统内部错误，请稍后重试或联系技术支持",
        503: "服务暂时不可用，请稍后重试"
    }

    # 操作类型转换
    operation_names = {
        "createInstance": "创建云服务器",
        "deleteInstance": "删除云服务器",
        "updateInstance": "更新云服务器",
        "createUser": "创建用户",
        "deleteUser": "删除用户",
        "updateUser": "修改用户信息",
        "attachRoleToUser": "给用户分配权限",
        "detachRoleFromUser": "撤销用户权限",
        "createAccessKey": "创建访问密钥",
        "deleteAccessKey": "删除访问密钥",
        "createSecurityGroup": "创建安全组",
        "deleteSecurityGroup": "删除安全组",
        "createSecurityGroupRule": "添加安全组规则",
        "deleteSecurityGroupRule": "删除安全组规则",
        "createVpc": "创建VPC",
        "deleteVpc": "删除VPC"
    }

    # 查找匹配的操作名
    friendly_operation = operation
    for key, value in operation_names.items():
        if key.lower() in operation.lower():
            friendly_operation = value
            break

    # 构建用户友好的说明
    message: Dict[str, Any] = {
        "时间": time_str,
        "操作人": user,
        "操作": friendly_operation,
        "资源": resource,
        "状态码": code_int
    }

    if code_int in error_messages:
        message["问题说明"] = error_messages[code_int]
    elif code_int >= 200 and code_int < 300:
        message["问题说明"] = "操作成功"
    else:
        message["问题说明"] = f"操作失败（错误码：{code_int}）"

    # 添加建议
    suggestions = {
        401: "请检查AK/SK配置，或联系管理员确认访问权限",
        403: "请联系管理员为您添加相应的操作权限",
        404: "请确认资源ID是否正确，或资源是否已被删除",
        409: "请等待其他操作完成后再试，或检查资源状态",
        500: "如问题持续，请联系华为云技术支持"
    }

    if code_int in suggestions:
        message["建议"] = suggestions[code_int]

    return message

def generate_report(analysis: Dict[str, Any], time_range: str, region: str) -> str:
    """生成检查报告"""
    report: List[str] = []
    report.append("=" * 60)
    report.append("异常检查报告")
    report.append("=" * 60)
    report.append(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"检查区域: {region}")
    report.append(f"时间范围: {time_range}")
    report.append("")

    # 异常统计 - 用户友好说明
    report.append("检查结果:")
    report.append("")

    total_anomalies = (analysis['by_rating'].get('warning', 0) + 
                       analysis['by_rating'].get('incident', 0) + 
                       len(analysis['failed_operations']))

    if total_anomalies == 0:
        report.append("✅ 未发现异常操作记录")
        report.append("   账号操作状态正常，未检测到警告或失败的操作")
    else:
        report.append(f"⚠️  发现 {total_anomalies} 个需要关注的问题：")
        report.append("")

        if analysis['by_rating'].get('warning', 0) > 0:
            report.append(f"   • 警告级别操作：{analysis['by_rating'].get('warning', 0)} 条")
            report.append("     说明：这些操作部分成功，可能存在配置问题")

        if analysis['by_rating'].get('incident', 0) > 0:
            report.append(f"   • 事故级别操作：{analysis['by_rating'].get('incident', 0)} 条")
            report.append("     说明：这些操作失败，可能存在安全风险")

        if len(analysis['failed_operations']) > 0:
            report.append(f"   • 失败的操作：{len(analysis['failed_operations'])} 条")
            report.append("     说明：这些操作返回错误，需要检查原因")
    report.append("")

    # 高风险操作 - 用户友好说明
    if analysis['sensitive_operations']:
        report.append("⚠️  敏感操作详情：")
        report.append("   这些操作涉及权限变更或安全配置，建议确认：")
        report.append("")
        for i, op in enumerate(analysis['sensitive_operations'][:5], 1):
            friendly_msg = generate_user_friendly_message(op)
            status = "✅" if op.get('rating') == 'normal' else "⚠️"
            report.append(f"   {i}. {status} {friendly_msg['操作']}")
            report.append(f"      时间：{friendly_msg['时间']}")
            report.append(f"      操作人：{friendly_msg['操作人']}")
            report.append(f"      资源：{friendly_msg['资源']}")
            report.append("")
        if len(analysis['sensitive_operations']) > 5:
            report.append(f"   ... 还有 {len(analysis['sensitive_operations']) - 5} 个敏感操作")
            report.append("")

    # 删除操作 - 用户友好说明
    if analysis['delete_operations']:
        report.append("🗑️  删除操作详情：")
        report.append("   这些操作删除了资源，请确认是否为预期操作：")
        report.append("")
        for i, op in enumerate(analysis['delete_operations'][:5], 1):
            friendly_msg = generate_user_friendly_message(op)
            status = "✅" if op.get('rating') == 'normal' else "⚠️"
            report.append(f"   {i}. {status} {friendly_msg['操作']}")
            report.append(f"      时间：{friendly_msg['时间']}")
            report.append(f"      操作人：{friendly_msg['操作人']}")
            report.append(f"      资源：{friendly_msg['资源']}")
            report.append("")
        if len(analysis['delete_operations']) > 5:
            report.append(f"   ... 还有 {len(analysis['delete_operations']) - 5} 个删除操作")
            report.append("")

    # 失败操作 - 用户友好说明
    if analysis['failed_operations']:
        report.append("❌ 失败的操作详情：")
        report.append("   这些操作未能成功执行，需要检查原因：")
        report.append("")
        for i, op in enumerate(analysis['failed_operations'][:5], 1):
            friendly_msg = generate_user_friendly_message(op)
            report.append(f"   {i}. {friendly_msg['操作']}")
            report.append(f"      时间：{friendly_msg['时间']}")
            report.append(f"      操作人：{friendly_msg['操作人']}")
            report.append(f"      问题：{friendly_msg['问题说明']}")
            if '建议' in friendly_msg:
                report.append(f"      建议：{friendly_msg['建议']}")
            report.append("")
        if len(analysis['failed_operations']) > 5:
            report.append(f"   ... 还有 {len(analysis['failed_operations']) - 5} 个失败操作")
            report.append("")

    # 服务分布
    if analysis['by_service']:
        report.append("服务分布:")
        for service, count in sorted(analysis['by_service'].items(), key=lambda x: x[1], reverse=True)[:10]:
            report.append(f"  - {service}: {count} 条")
        report.append("")

    # 用户分布
    if analysis['by_user']:
        report.append("用户分布:")
        for user, count in sorted(analysis['by_user'].items(), key=lambda x: x[1], reverse=True)[:10]:
            report.append(f"  - {user}: {count} 条")
        report.append("")

    # 建议 - 用户友好说明
    report.append("处理建议：")
    report.append("")

    if total_anomalies == 0:
        report.append("✅ 账号状态良好，建议：")
        report.append("   • 定期检查CTS日志（建议每周一次）")
        report.append("   • 关注敏感操作的执行情况")
    else:
        if analysis['by_rating'].get('incident', 0) > 0:
            report.append("🔴 高优先级：")
            report.append("   • 立即检查事故级别记录，确认是否存在安全问题")
            report.append("   • 如发现未授权操作，立即修改权限并通知相关人员")
            report.append("")

        if len(analysis['failed_operations']) > 0:
            report.append("🟡 中优先级：")
            report.append("   • 分析失败操作的具体原因")
            report.append("   • 检查相关用户的权限配置")
            report.append("   • 确认是否存在配置错误")
            report.append("")

        if len(analysis['sensitive_operations']) > 0:
            report.append("🟡 需要确认：")
            report.append("   • 审查敏感操作是否经过授权")
            report.append("   • 确认权限变更是否符合预期")
            report.append("   • 检查密钥创建是否为预期操作")
            report.append("")

        if len(analysis['delete_operations']) > 0:
            report.append("🟡 需要确认：")
            report.append("   • 确认删除操作是否为预期操作")
            report.append("   • 检查是否误删重要资源")
            report.append("   • 如有误删，及时恢复数据")
            report.append("")

    report.append("")
    report.append("=" * 60)

    return "\n".join(report)

class HuaweiCloudSigner:
    def __init__(self, ak: str, sk: str, security_token: str):
        self.ak = ak
        self.sk = sk
        self.security_token = security_token

    def _hmac_sha256(self, key: str, msg: str):
        """计算 HMAC-SHA256"""
        return hmac.new(key.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).digest()

    def _hash_sha256(self, msg: str):
        """计算 SHA256 哈希"""
        return hashlib.sha256(msg.encode('utf-8')).hexdigest()  #.lower()

    def sign_request(self, method: str, endpoint: str, path: str, query_params: Optional[Dict[str, Any]]=None, body: str=''):
        """
        对请求进行签名
        :param method: HTTP 方法，如 'GET'
        :param endpoint: 服务端点，如 'ecs.cn-north-1.myhuaweicloud.com'
        :param path: 请求路径，如 '/v1/project-id/servers'
        :param query_params: 查询参数字典
        :param body: 请求体字符串（JSON 或空字符串）
        :return: 构造好的 urllib.request.Request 对象
        """

        # 生成时间戳（必须使用 UTC 时间）
        t = datetime.now(timezone.utc)
        x_sdk_date = t.strftime('%Y%m%dT%H%M%SZ')

        # 处理查询参数（按字典序排序并编码）
        if query_params:
            sorted_params = sorted(query_params.items())
            encoded_params = [f"{quote(k, safe='')}={quote(str(v), safe='')}" for k, v in sorted_params]
            query_string = '&'.join(encoded_params)
            full_uri = f"{path}?{query_string}"
        else:
            query_string = ''
            full_uri = path

        headers: Dict[str, str] = {
            'Host': endpoint,
            'X-Sdk-Date': x_sdk_date,
            'X-Security-Token': self.security_token,  # 临时 AK/SK 必须携带此头
        }

        __signed_headers: List[str] = []
        __headers: Dict[str, str] = {}
        for key in headers.keys():
            if "_" in key:
                continue
            key_encoded = key.lower()
            value = headers[key]
            value_encoded = str(value).strip()
            __headers[key_encoded] = value_encoded
            headers[key] = value_encoded.encode('utf-8').decode('iso-8859-1')
            __signed_headers.append(key_encoded)
        __signed_headers.sort()

        canonical_headers = '\n'.join([f"{key}:{__headers.get(key)}" for key in __signed_headers]) + '\n'
        signed_headers = ';'.join(__signed_headers)

        # canonical_headers = f"host:{endpoint}\nx-sdk-date:{x_sdk_date}\nx-security-token:{self.security_token}\n"
        # signed_headers = "host;x-sdk-date;x-security-token"

        # 构造规范请求（CanonicalRequest）
        hashed_payload = self._hash_sha256(body) if body else self._hash_sha256('')
        canonical_uri = path if path.endswith('/') else path + '/'

        canonical_request: str = '\n'.join([
            method.upper(),
            canonical_uri,
            query_string,
            canonical_headers,
            signed_headers,
            hashed_payload
        ])

        # 构造待签字符串（StringToSign）
        string_to_sign = f"SDK-HMAC-SHA256\n{x_sdk_date}\n{self._hash_sha256(canonical_request)}"

        # 计算签名
        signature = hmac.new(self.sk.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

        # 构造 Authorization
        auth_header = f"SDK-HMAC-SHA256 Access={self.ak}, SignedHeaders={signed_headers}, Signature={signature}"
        headers['Authorization'] = auth_header

        # 创建并返回 Request 对象
        req = urllib.request.Request(url=f"https://{endpoint}{full_uri}", headers=headers, method=method.upper())
        if body and method.upper() in ['POST', 'PUT']:
            req.data = body.encode('utf-8')
        return req

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="异常检查")
    parser.add_argument("--region", required=True, help="区域")
    parser.add_argument("--project-id", required=True, help="项目ID")
    parser.add_argument("--hours", type=int, default=24, help="查询最近N小时 (默认24)")
    parser.add_argument("--limit", type=int, default=200, help="最大记录数 (默认200)")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")

    args = parser.parse_args()

    credential = run_hcloud("IAM", "CreateTemporaryAccessKeyByToken/v3", {
        "cli-region": args.region,
        "auth.identity.methods.1": "token",
        "auth.identity.token.duration_seconds": 86400
    })
    if "error" in credential or "credential" not in credential:
        print("获取临时访问密钥失败")
        sys.exit(-1)

    # 配置你的临时凭证（从 CreateTemporaryAccessKeyByToken 响应中获取）
    credential: Dict[str, Any] = credential["credential"]
    ak = credential["access"]  # 临时 Access Key
    sk = credential["secret"]  # 临时 Secret Key
    security_token = credential["securitytoken"]  # 安全令牌

    # 创建签名器
    signer = HuaweiCloudSigner(ak, sk, security_token)

    # 查询账单
    endpoint = "bss.cn-north-1.myhuaweicloud.com"
    path = "/v2/accounts/customer-accounts/balances"
    req = signer.sign_request(method='GET', endpoint=endpoint, path=path)
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            if(json.loads(result).get('debt_amount', 0) > 0):
                print("警告：您的账号已欠费，无法正常购买和使用按需计费云服务，请您尽快充值。\n")
    except urllib.error.HTTPError as e:
        print(f"查询账单失败: {e.code} {e.reason}")

    # 直接查询所有记录（不传时间参数）
    all_traces_result = query_traces(args.region, args.project_id, limit=args.limit)

    if "error" in all_traces_result:
        # 查询失败
        print("=" * 60)
        print("异常检查报告")
        print("=" * 60)
        print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"检查区域: {args.region}")
        print()
        print("❌ 无法查询操作记录")
        print()
        print("问题说明：")
        print(f"  {all_traces_result['error']}")
        print()
        print("可能原因：")
        print("  • CTS追踪器未启用或未正常工作")
        print("  • 查询时间范围内没有操作记录")
        print("  • 权限不足，无法查询追踪记录")
        print("  • 服务暂时不可用")
        print()
        print("建议措施：")
        print("  1. 检查CTS服务是否已启用")
        print("  2. 确认是否有足够的查询权限")
        print("  3. 稍后重试或联系技术支持")
        print()
        print("=" * 60)
        sys.exit(0)

    all_traces = all_traces_result.get("traces", [])

    # 计算时间范围（从返回的数据中）
    if all_traces:
        times = [t.get('time', 0) for t in all_traces]
        if times:
            min_time = datetime.fromtimestamp(min(times) / 1000)
            max_time = datetime.fromtimestamp(max(times) / 1000)
            time_range = f"{min_time.strftime('%Y-%m-%d %H:%M')} 至 {max_time.strftime('%Y-%m-%d %H:%M')}"
        else:
            time_range = "未知"
    else:
        time_range = "无记录"

    # 查询警告记录
    warning_traces_result = query_traces(args.region, args.project_id, 
                                         trace_rating="warning",
                                         limit=args.limit)
    warning_traces = warning_traces_result.get("traces", [])

    # 查询事故记录
    incident_traces_result = query_traces(args.region, args.project_id, 
                                          trace_rating="incident",
                                          limit=args.limit)
    incident_traces = incident_traces_result.get("traces", [])

    # 合并所有记录
    all_traces.extend(warning_traces)
    all_traces.extend(incident_traces)

    # 去重
    seen_ids = set()
    unique_traces = []
    for trace in all_traces:
        trace_id = trace.get("trace_id")
        if trace_id and trace_id not in seen_ids:
            seen_ids.add(trace_id)
            unique_traces.append(trace)

    # 分析
    analysis = analyze_traces(unique_traces)

    # 输出
    if args.output == "json":
        output = {
            "check_time": datetime.now().isoformat(),
            "region": args.region,
            "time_range": time_range,
            "analysis": analysis
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        report = generate_report(analysis, time_range, args.region)
        print(report)


if __name__ == "__main__":
    main()
