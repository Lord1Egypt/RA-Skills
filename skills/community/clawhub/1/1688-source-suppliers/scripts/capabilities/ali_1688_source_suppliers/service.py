#!/usr/bin/env python3
"""1688供应商信息"""

import json

from _http import api_post_stream
from _errors import ServiceError


def query_1688_source_suppliers(query: str) -> dict:
    """查询1688供应商信息（流式）"""
    
    full_content = api_post_stream("/api/1688_source_suppliers/1.0.0", {"query": query})
    
    try:
        result = json.loads(full_content)
        
        if not result.get("success"):
            msg_info = result.get("msgInfo", "未知错误")
            raise ServiceError(f"API调用失败: {msg_info}")
            
        factories_info = _extract_factories_from_response(result)
        markdown_output = _generate_markdown_output(factories_info)
        
        return {
            "factories": factories_info,
            "markdown": markdown_output
        }
            
    except json.JSONDecodeError as e:
        raise ServiceError(f"数据解析失败: {e}")


def _parse_json_field(field_value: str) -> list:
    """解析 JSON 数组字段，例如: "[\"OEM\",\"ODM\"]" -> ["OEM", "ODM"]"""
    if not field_value:
        return []
    try:
        result = json.loads(field_value)
        return result if isinstance(result, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _find_retrieval_data(data_list: list) -> list:
    """从列表中查找 RETRIEVAL 阶段的数据"""
    for item in data_list:
        if isinstance(item, dict) and item.get("currentPhase") == "RETRIEVAL":
            response_data = item.get("responseData", {})
            if isinstance(response_data, dict) and "data" in response_data:
                factories = response_data["data"]
                if isinstance(factories, list) and len(factories) > 0:
                    return factories
    return []


def _get_factories_data(result: dict) -> list:
    """从API响应中获取工厂数据列表
    
    支持三种数据格式：
    1. 顶层 originResponses 数组
    2. data.result.originResponses 数组
    3. data.result.model 数组
    """
    # 格式1 & 格式2：originResponses
    origin_responses = result.get("originResponses", [])
    if not origin_responses:
        origin_responses = result.get("data", {}).get("result", {}).get("originResponses", [])
    
    factories = _find_retrieval_data(origin_responses)
    if factories:
        return factories
    
    # 格式3：data.result.model
    model = result.get("data", {}).get("result", {}).get("model", [])
    if isinstance(model, list):
        factories = _find_retrieval_data(model)
        if factories:
            return factories
    
    return []


def _extract_factories_from_response(result: dict) -> list:
    """从API响应中提取所有工厂信息"""
    try:
        factories = _get_factories_data(result)
        
        extracted_factories = []
        for factory in factories:
            if not isinstance(factory, dict):
                continue
            
            ext_infos = factory.get("extInfos", {})
            
            # 基础信息
            company_name = factory.get("companyName", "")
            oem_mode = _parse_json_field(ext_infos.get("oem_mode", ""))
            manufacture_type = _parse_json_field(ext_infos.get("manufacture_type", ""))
            
            # 数据质量过滤
            if not company_name or not oem_mode or not manufacture_type:
                continue
            
            # 所在地区
            province = ext_infos.get("reg_prov_name", "")
            city = ext_infos.get("reg_city_name", "")
            location = f"{province}{city}" if province or city else ""
            
            extracted_factories.append({
                "companyName": company_name,
                "companyUrl": factory.get("companyUrl", ""),
                "cooperationMode": oem_mode,
                "services": manufacture_type,
                "location": location,
                "factoryLevel": ext_infos.get("factory_level", ""),
                "factoryType": _parse_json_field(ext_infos.get("factory_type_tag", [])),
                "recTags": _parse_json_field(ext_infos.get("rec_tags", [])),
                "satisfiedRate": ext_infos.get("satisfied_rate_std_001", ""),
                "monthlyOrders": ext_infos.get("pay_ord_byr_cnt_1m_004", 0),
                "supportProofing": ext_infos.get("is_proofing", "") == "Y",
                "score": factory.get("score", 0)
            })
        
        return extracted_factories
        
    except Exception as e:
        raise ServiceError(f"提取工厂信息失败: {e}")


def _generate_markdown_output(factories: list) -> str:
    """生成展示用的Markdown输出，公司名称可点击跳转"""
    if not factories:
        return "未找到供应商信息"
    
    parts = [f"找到 {len(factories)} 家供应商\n"]
    
    for i, f in enumerate(factories, 1):
        lines = [f"---\n\n### 供应商 {i}\n"]
        
        # 公司名称（可点击链接）
        company_name = f.get("companyName", "")
        company_url = f.get("companyUrl", "")
        if company_url and company_name:
            lines.append(f"- 公司名称: [{company_name}]({company_url})")
        else:
            lines.append(f"- 公司名称: {company_name}")
        
        # 所在地区
        location = f.get("location", "")
        if location:
            lines.append(f"- 所在地区: {location}")
        
        # 工厂信息
        factory_info = []
        if f.get("factoryLevel"):
            factory_info.append(f["factoryLevel"])
        factory_type = ", ".join(f.get("factoryType", []))
        if factory_type:
            factory_info.append(factory_type)
        if factory_info:
            lines.append(f"- 工厂信息: {', '.join(factory_info)}")
        
        # 推荐标签
        rec_tags = ", ".join(f.get("recTags", []))
        if rec_tags:
            lines.append(f"- 推荐标签: {rec_tags}")
        
        # 服务指标
        indicators = []
        if f.get("satisfiedRate"):
            indicators.append(f["satisfiedRate"])
        if f.get("monthlyOrders"):
            indicators.append(f"月订单{f['monthlyOrders']}单")
        if f.get("supportProofing"):
            indicators.append("支持打样")
        if indicators:
            lines.append(f"- 服务指标: {', '.join(indicators)}")
        
        # 合作方式和服务
        lines.append(f"- 合作方式: {', '.join(f.get('cooperationMode', []))}")
        lines.append(f"- 服务: {', '.join(f.get('services', []))}")
        
        parts.append("\n".join(lines) + "\n")
    
    return "\n".join(parts)
