#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LLM语义匹配脚本 (2026-05, v3)
功能：使用腾讯混元/字节豆包API增强定额语义理解
用法：python llm_semantic_match.py "热泵安装" "第2册热力设备"

默认模型：腾讯混元 Hunyuan-Lite（免费，无限制）
备选模型：字节豆包（按需开启，需设置 LLM_PROVIDER=doubao）

所有模型统一走 OpenAI 兼容接口（HTTP + requests），无需SDK依赖。
混元降级策略：混元失败时自动降级到豆包（如已配置）。
"""

import os
import json
import sys
import re
import requests
from typing import List, Dict, Optional
from pathlib import Path

# ============================================================
# API配置
# ============================================================

# 默认使用混元（免费），豆包作为备选
USE_PROVIDER = os.getenv("LLM_PROVIDER", "hunyuan")  # "hunyuan"（默认）或 "doubao"

# --- 腾讯混元配置（默认，免费）---
HUNYUAN_SECRET_ID = os.getenv("HUNYUAN_SECRET_ID", "")
HUNYUAN_SECRET_KEY = os.getenv("HUNYUAN_SECRET_KEY", "")
HUNYUAN_API_KEY = os.getenv("HUNYUAN_API_KEY", "")  # 可选：混元OpenAI兼容接口的API Key（sk-开头）
HUNYUAN_MODEL = "hunyuan-lite"

# --- 豆包配置（备选，按需开启）---
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY", "")
DOUBAO_ENDPOINT_ID = os.getenv("DOUBAO_ENDPOINT_ID", "")  # 豆包接入点ID（Ark平台获取）
DOUBAO_MODEL = "doubao-1-5-lite-32k-250115"

# Temperature设置（0=确定性输出，推荐）
TEMPERATURE = 0.0

# ============================================================
# 定额分册信息（用于LLM理解专业背景）
# ============================================================

INSTALL_ENGINEERING_VOLUMES = """
安装工程13分册（2025版山东省消耗量定额）：
- 第1册 机械设备安装工程：泵、风机、制冷设备
- 第2册 热力设备安装工程：锅炉、热泵、换热站
- 第3册 静置设备与工艺金属结构：容器、塔器、储罐
- 第4册 电气设备安装工程：变配电、电缆、照明
- 第5册 建筑智能化工程：综合布线、安防、楼宇自控
- 第6册 自动化控制仪表安装工程：工业自动化仪表
- 第7册 通风空调工程：风管、风机、空调机组
- 第8册 工业管道工程：高温高压管道、焊接、试压
- 第9册 消防工程：自动喷淋、火灾报警
- 第10册 给排水、采暖、燃气工程：室内外给排水、散热器
- 第11册 通信设备与线缆安装工程
- 第12册 刷油、防腐蚀、绝热工程
- 第13册 措施项目：脚手架、高层增加费
"""

# ============================================================
# 系统提示词（用于LLM理解任务）
# ============================================================

SYSTEM_PROMPT = f"""你是一名专业的山东省安装工程造价工程师，擅长定额匹配和组价计算。

## 你的任务
根据用户描述的工作内容，判断所属分册并提取搜索关键词，供本地定额数据库查询。

## 定额分册参考
{INSTALL_ENGINEERING_VOLUMES}

## 严格禁止
你不得编造、猜测或推断任何定额编号！你不知道定额库中有哪些真实编号。
所有定额编号必须由本地数据库查询返回，你不能直接生成编号。

## 你的正确任务
1. 判断工作内容属于哪个分册
2. 提取3~5个搜索关键词（用于本地定额数据库查询）
3. 识别设备类型、规格参数
4. 列出通常需要的辅定额类别（描述性，不给编号）

## 输出格式要求
严格按以下JSON格式输出，不要添加任何解释性文字：
{{
    "volume": "第X册 XXX工程",
    "search_keywords": ["关键词1", "关键词2", "关键词3"],
    "equipment_type": "设备类型（如：活塞式压缩机、离心式冷水机组）",
    "spec_params": {{
        "参数名": "参数值"
    }},
    "auxiliary_categories": [
        "辅定额类别描述（如：管道试压、除锈刷油）"
    ],
    "main_materials": [
        {{
            "name": "主材名称",
            "spec": "规格型号",
            "unit": "单位",
            "loss_rate": 0.02
        }}
    ],
    "confidence": 0.95,
    "reasoning": "简要说明判断依据"
}}

## 注意事项
1. 搜索关键词应从用户描述中提取，尽量使用定额库中可能出现的术语
2. 如果用户描述模糊，confidence设为0.5并在reasoning中说明
3. 只输出JSON，不要输出其他内容
4. 损耗率参考：管道/管件2%、电缆5%、钢材3%、设备1%
"""


# ============================================================
# 通用LLM调用函数
# ============================================================

def _call_openai_compatible(url: str, api_key: str, model: str,
                            user_input: str, volume_hint: str = "",
                            provider_name: str = "") -> Optional[Dict]:
    """
    通用 OpenAI 兼容接口调用

    Args:
        url: API endpoint URL
        api_key: Bearer token
        model: 模型名称
        user_input: 用户输入
        volume_hint: 分册提示
        provider_name: 提供商名称（用于错误信息）
    """
    try:
        user_msg = f"工作内容：{user_input}\n分册提示：{volume_hint}" if volume_hint else f"工作内容：{user_input}"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            "temperature": TEMPERATURE
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            # 清理可能的markdown代码块包裹
            content = re.sub(r'^```json\s*', '', content.strip())
            content = re.sub(r'\s*```$', '', content.strip())
            return json.loads(content)
        else:
            error_msg = result.get("error", {}).get("message", str(result))
            print(f"{provider_name}API返回异常：{error_msg}")
            return None

    except requests.exceptions.Timeout:
        print(f"{provider_name}API调用超时（30秒）")
        return None
    except requests.exceptions.ConnectionError:
        print(f"{provider_name}API连接失败，请检查网络")
        return None
    except json.JSONDecodeError as e:
        print(f"{provider_name}API返回内容JSON解析失败：{e}")
        return None
    except Exception as e:
        print(f"{provider_name}API调用失败：{e}")
        return None


# ============================================================
# 腾讯混元API调用（默认，免费）
# ============================================================

def _generate_hunyuan_token(secret_id: str, secret_key: str) -> str:
    """
    生成腾讯混元 OpenAI 兼容接口的临时 API Key（Bearer Token）
    使用腾讯云 API 签名 v3 生成临时凭证

    注意：如果已配置 HUNYUAN_API_KEY（sk-开头），可直接使用，无需此函数
    """
    import hashlib
    import hmac
    import base64
    import time
    from datetime import datetime, timezone

    # 混元 OpenAI 兼容接口需要通过腾讯云签名生成临时 token
    # 简化实现：使用 SecretId:SecretKey 作为 Basic Auth
    return f"{secret_id}:{secret_key}"


def call_hunyuan_api(user_input: str, volume_hint: str = "") -> Optional[Dict]:
    """调用腾讯混元API（Hunyuan-Lite，完全免费）"""
    # 优先使用 OpenAI 兼容接口（需要 sk- 开头的 HUNYUAN_API_KEY）
    if HUNYUAN_API_KEY:
        return _call_openai_compatible(
            url="https://api.hunyuan.cloud.tencent.com/v1/chat/completions",
            api_key=HUNYUAN_API_KEY,
            model=HUNYUAN_MODEL,
            user_input=user_input,
            volume_hint=volume_hint,
            provider_name="混元"
        )

    # 降级：使用腾讯云 SDK 方式调用（需要 CAM 权限）
    try:
        from tencentcloud.hunyuan.v20230901 import hunyuan_client, models as hunyuan_models
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.common.credential import Credential

        if not HUNYUAN_SECRET_ID or not HUNYUAN_SECRET_KEY:
            print("错误：未设置 HUNYUAN_API_KEY 环境变量")
            print("获取地址：https://console.cloud.tencent.com/hunyuan/start")
            print("步骤：")
            print("  1. 登录 https://console.cloud.tencent.com/hunyuan/settings 开通混元服务")
            print("  2. 进入 https://console.cloud.tencent.com/hunyuan/start 创建 API Key（sk-开头）")
            print("  3. 设置环境变量：set HUNYUAN_API_KEY=sk-xxx")
            return None

        # 初始化客户端
        httpProfile = HttpProfile()
        httpProfile.endpoint = "hunyuan.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        cred = Credential(HUNYUAN_SECRET_ID, HUNYUAN_SECRET_KEY)
        client = hunyuan_client.HunyuanClient(cred, "ap-guangzhou", clientProfile)

        # 构建请求
        req = hunyuan_models.ChatCompletionsRequest()
        user_msg = f"工作内容：{user_input}\n分册提示：{volume_hint}" if volume_hint else f"工作内容：{user_input}"
        req.from_json_string(json.dumps({
            "Model": HUNYUAN_MODEL,
            "Messages": [
                {"Role": "system", "Content": SYSTEM_PROMPT},
                {"Role": "user", "Content": user_msg}
            ],
            "Temperature": TEMPERATURE
        }))

        # 调用API
        resp = client.ChatCompletions(req)
        resp_json = json.loads(resp.to_json_string())

        if "Choices" in resp_json and len(resp_json["Choices"]) > 0:
            content = resp_json["Choices"][0]["Message"]["Content"]
            content = re.sub(r'^```json\s*', '', content.strip())
            content = re.sub(r'\s*```$', '', content.strip())
            return json.loads(content)
        else:
            print(f"混元API返回格式异常：{resp_json}")
            return None

    except Exception as e:
        err_str = str(e)
        if "UnauthorizedOperation" in err_str or "not authorized" in err_str.lower():
            print("混元API权限不足，请检查：")
            print("  1. 是否已开通混元服务：https://console.cloud.tencent.com/hunyuan/settings")
            print("  2. CAM策略是否已授权 hunyuan:ChatCompletions 操作")
            print("  3. 或者配置 HUNYUAN_API_KEY（sk-开头）使用OpenAI兼容接口")
        else:
            print(f"混元API调用失败：{e}")
        return None


# ============================================================
# 豆包API调用（备选，按需开启）
# ============================================================

def call_doubao_api(user_input: str, volume_hint: str = "") -> Optional[Dict]:
    """调用豆包API（备选，需设置DOUBAO_API_KEY）"""
    if not DOUBAO_API_KEY:
        print("错误：未设置DOUBAO_API_KEY环境变量")
        print("获取地址：https://console.volcengine.com/ark")
        print("切换到混元（默认）：set LLM_PROVIDER=hunyuan")
        return None

    # 使用 Endpoint ID 优先（豆包方舟平台推荐方式）
    model = DOUBAO_ENDPOINT_ID if DOUBAO_ENDPOINT_ID else DOUBAO_MODEL

    return _call_openai_compatible(
        url="https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        api_key=DOUBAO_API_KEY,
        model=model,
        user_input=user_input,
        volume_hint=volume_hint,
        provider_name="豆包"
    )


# ============================================================
# 便捷切换函数（供外部脚本调用）
# ============================================================

def enable_llm():
    """启用LLM功能（已默认开启，保留兼容）"""
    print("LLM语义匹配功能已开启（默认使用腾讯混元）")

def use_hunyuan():
    """切换到腾讯混元（免费）"""
    global USE_PROVIDER
    USE_PROVIDER = "hunyuan"
    os.environ["LLM_PROVIDER"] = "hunyuan"
    print("已切换到腾讯混元 Hunyuan-Lite（免费）")

def use_doubao():
    """切换到豆包模型（备选）"""
    global USE_PROVIDER
    USE_PROVIDER = "doubao"
    os.environ["LLM_PROVIDER"] = "doubao"
    print("已切换到字节豆包（备选）")

def switch_model(provider: str):
    """通过字符串切换模型"""
    if provider == "hunyuan":
        use_hunyuan()
    elif provider == "doubao":
        use_doubao()
    else:
        print(f"不支持的模型：{provider}，可选：hunyuan / doubao")

def restore_default():
    """恢复默认（混元）"""
    use_hunyuan()

def get_current_provider() -> str:
    """获取当前使用的模型"""
    return USE_PROVIDER


# ============================================================
# 本地定额库验证（防LLM幻觉核心模块）
# ============================================================

def _get_searcher():
    """延迟加载搜索器（避免每次调用都重新加载索引）"""
    if not hasattr(_get_searcher, '_instance'):
        try:
            search_path = Path(__file__).parent / "search_quota.py"
            import importlib.util
            spec = importlib.util.spec_from_file_location("search_quota", search_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _get_searcher._instance = mod.QuotaSearcher()
        except Exception as e:
            print(f"⚠ 本地索引加载失败：{e}")
            _get_searcher._instance = None
    return _get_searcher._instance


def verify_quota_code(code: str) -> dict:
    """
    在本地定额库中验证定额编号是否存在
    
    Args:
        code: 定额编号（如 "8-3-28"）
    
    Returns:
        {'exists': True, 'data': {...}} 或 {'exists': False, 'data': None}
    """
    searcher = _get_searcher()
    if not searcher:
        return {'exists': False, 'data': None, 'error': '索引未加载'}
    
    results = searcher.search_by_quota_no(code)
    if results:
        return {'exists': True, 'data': results[0]}
    return {'exists': False, 'data': None}


def local_search_by_keywords(keywords: list, volume: str = "", top_k: int = 15) -> list:
    """
    用关键词在本地定额库搜索
    
    Args:
        keywords: 搜索关键词列表
        volume: 分册过滤（如"第8册"）
        top_k: 每个关键词返回条数
    
    Returns:
        去重后的搜索结果列表
    """
    searcher = _get_searcher()
    if not searcher:
        return []
    
    all_results = []
    seen = set()
    
    for kw in keywords:
        try:
            results = searcher.search(kw, top_k=top_k, volume=volume)
            for r in results:
                code = r.get("quota_no", "")
                if code and code not in seen:
                    seen.add(code)
                    all_results.append(r)
        except Exception:
            continue
    
    return all_results


def hybrid_search(user_input: str, volume_hint: str = "") -> dict:
    """
    LLM辅助 + 本地验证的混合搜索（防幻觉核心函数）
    
    流程：
    1. LLM提取搜索意图（分册、关键词、设备类型）
    2. 本地库按关键词搜索
    3. 返回全部真实结果（编号100%可信）
    
    Args:
        user_input: 用户描述的工作内容
        volume_hint: 可选的分册提示
    
    Returns:
        {
            'source': 'hybrid',
            'llm_analysis': {...},  # LLM的分析结果
            'verified_results': [...],  # 本地库验证后的真实结果
            'total_found': int
        }
    """
    provider_display = "腾讯混元" if USE_PROVIDER == "hunyuan" else "字节豆包"
    print(f"正在执行混合搜索（LLM辅助 + 本地验证）...")
    print(f"  工作内容：{user_input}")
    print(f"  分册提示：{volume_hint or '自动识别'}")
    print(f"  当前模型：{provider_display}")
    print()
    
    # Step 1: 调用LLM提取搜索意图
    if USE_PROVIDER == "hunyuan":
        llm_result = call_hunyuan_api(user_input, volume_hint)
    else:
        llm_result = call_doubao_api(user_input, volume_hint)
    
    # 混元失败降级到豆包
    if not llm_result and USE_PROVIDER == "hunyuan" and DOUBAO_API_KEY:
        print("混元调用失败，尝试降级到豆包...")
        llm_result = call_doubao_api(user_input, volume_hint)
    
    if not llm_result:
        # LLM完全失败，直接用用户输入作为关键词进行本地搜索
        print("⚠ LLM调用失败，直接使用用户输入进行本地搜索")
        keywords = [user_input]
        volume = volume_hint
        llm_analysis = {"source": "fallback", "volume": volume}
    else:
        # 提取LLM分析结果
        keywords = llm_result.get("search_keywords", [user_input])
        volume = llm_result.get("volume", volume_hint)
        llm_analysis = {
            "source": "llm",
            "volume": llm_result.get("volume"),
            "equipment_type": llm_result.get("equipment_type", ""),
            "spec_params": llm_result.get("spec_params", {}),
            "auxiliary_categories": llm_result.get("auxiliary_categories", []),
            "confidence": llm_result.get("confidence", 0),
            "reasoning": llm_result.get("reasoning", "")
        }
        print(f"  LLM分析：分册={volume}, 类型={llm_analysis.get('equipment_type','未知')}")
        print(f"  搜索关键词：{keywords}")
        print()
    
    # Step 2: 本地库搜索（真实数据）
    verified_results = local_search_by_keywords(keywords, volume, top_k=15)
    
    # Step 3: 格式化输出
    print("=" * 60)
    print("混合搜索结果（本地库验证，编号100%真实）")
    print("=" * 60)
    
    if verified_results:
        for i, r in enumerate(verified_results, 1):
            print(f"\n  {i}. {r.get('quota_no', 'N/A')} | {r.get('name', 'N/A')}")
            print(f"     单位: {r.get('unit', 'N/A')} | 基价: {r.get('base_price', 'N/A')}元")
            print(f"     分册: {r.get('volume', 'N/A')} | 章节: {r.get('chapter', 'N/A')}")
    else:
        print("\n  ⚠️ 未在本地定额库中找到匹配结果")
        print("  建议：尝试更换关键词或检查分册范围")
    
    print(f"\n共找到 {len(verified_results)} 条真实定额")
    print("=" * 60)
    
    return {
        "source": "hybrid",
        "llm_analysis": llm_analysis,
        "verified_results": verified_results,
        "total_found": len(verified_results),
        "main_materials": llm_result.get("main_materials", []) if llm_result else []
    }


# ============================================================
# 语义匹配主函数
# ============================================================

def semantic_match(user_input: str, volume_hint: str = "") -> Dict:
    """
    语义匹配主函数（带本地验证防幻觉）

    Args:
        user_input: 用户描述的工作内容（如"热泵安装"）
        volume_hint: 分册提示（如"第2册热力设备"）

    Returns:
        包含推荐定额的字典（所有编号均经过本地库验证）
    """
    provider_display = "腾讯混元 Hunyuan-Lite" if USE_PROVIDER == "hunyuan" else "字节豆包"
    print(f"正在调用LLM进行语义匹配...")
    print(f"  工作内容：{user_input}")
    print(f"  分册提示：{volume_hint or '自动识别'}")
    print(f"  当前模型：{provider_display}")
    print()

    # 根据配置选择API
    if USE_PROVIDER == "hunyuan":
        result = call_hunyuan_api(user_input, volume_hint)
    else:
        result = call_doubao_api(user_input, volume_hint)

    # 如果混元失败，尝试豆包作为降级
    if not result and USE_PROVIDER == "hunyuan" and DOUBAO_API_KEY:
        print("混元调用失败，尝试降级到豆包...")
        result = call_doubao_api(user_input, volume_hint)

    if not result:
        print("LLM调用失败，请检查API配置")
        print("当前配置：")
        print(f"  模型：{USE_PROVIDER}")
        print(f"  混元SecretId：{'已配置' if HUNYUAN_SECRET_ID else '未配置'}")
        print(f"  混元API Key（sk-）：{'已配置' if HUNYUAN_API_KEY else '未配置'}")
        print(f"  豆包API Key：{'已配置' if DOUBAO_API_KEY else '未配置'}")
        print(f"  豆包Endpoint ID：{'已配置' if DOUBAO_ENDPOINT_ID else '未配置（将使用模型名）'}")
        return {}

    # ========== 核心改进：本地库交叉验证 ==========
    # 模式一：LLM返回搜索关键词模式（新提示词格式）
    if "search_keywords" in result:
        # 新模式：LLM只输出关键词，用本地库搜索真实数据
        print("  [验证模式] LLM提取关键词 → 本地库搜索")
        keywords = result.get("search_keywords", [])
        volume = result.get("volume", volume_hint)
        
        verified_results = local_search_by_keywords(keywords, volume, top_k=15)
        
        # 格式化输出
        print("=" * 60)
        print("语义匹配结果（本地库验证通过）")
        print("=" * 60)
        
        print(f"\n【LLM分析】")
        print(f"  分册定位：{result.get('volume', volume_hint or '未知')}")
        print(f"  设备类型：{result.get('equipment_type', '未知')}")
        print(f"  规格参数：{result.get('spec_params', {})}")
        print(f"  判断依据：{result.get('reasoning', '无')}")
        
        if verified_results:
            print(f"\n【本地库匹配结果】共 {len(verified_results)} 条")
            for i, r in enumerate(verified_results[:10], 1):
                print(f"  {i}. {r.get('quota_no', 'N/A')} | {r.get('name', 'N/A')}")
                print(f"     单位:{r.get('unit','N/A')} 基价:{r.get('base_price','N/A')}元 章节:{r.get('chapter','N/A')}")
            if len(verified_results) > 10:
                print(f"  ... 还有 {len(verified_results) - 10} 条")
        else:
            print(f"\n  ⚠️ 本地库未找到匹配，建议更换关键词")
        
        if result.get("auxiliary_categories"):
            print(f"\n【建议辅定额类别】")
            for cat in result["auxiliary_categories"]:
                print(f"  - {cat}")
        
        if result.get("main_materials"):
            print(f"\n【主材】")
            for m in result["main_materials"]:
                print(f"  - {m.get('name', 'N/A')} {m.get('spec', '')} (损耗率:{m.get('loss_rate', 0)*100:.1f}%)")
        
        print(f"\n置信度：{result.get('confidence', 0)*100:.0f}%")
        print("=" * 60)
        
        # 返回增强结果
        result["verified_results"] = verified_results
        result["verification_status"] = "keyword_search"
        return result
    
    # 模式二：兼容旧格式（LLM仍返回定额编号时的验证）
    elif "main_quota" in result:
        # 旧模式：LLM直接输出了编号，必须验证！
        code = result["main_quota"].get("code", "")
        print(f"  [验证模式] LLM返回编号 → 本地库校验")
        
        verification = verify_quota_code(code)
        if verification["exists"]:
            # 编号存在，补充真实基价数据
            real_data = verification["data"]
            result["main_quota"]["base_price"] = real_data.get("base_price")
            result["main_quota"]["chapter"] = real_data.get("chapter")
            result["verification_status"] = "verified"
            
            print("=" * 60)
            print("语义匹配结果（本地库验证通过 ✅）")
            print("=" * 60)
            
            mq = result["main_quota"]
            print(f"\n【主定额】")
            print(f"  定额编号：{mq.get('code', 'N/A')}")
            print(f"  定额名称：{mq.get('name', 'N/A')}")
            print(f"  所属分册：{mq.get('volume', 'N/A')}")
            print(f"  章节：{mq.get('chapter', 'N/A')}")
            print(f"  计量单位：{mq.get('unit', 'N/A')}")
            print(f"  基价：{mq.get('base_price', 'N/A')} 元")
            print(f"  匹配理由：{mq.get('reason', 'N/A')}")
        else:
            # 编号不存在！触发本地搜索修正
            print(f"\n  ⚠️ 警告：LLM返回的编号 [{code}] 在本地库中不存在！")
            print("  正在用LLM推荐的关键词进行本地搜索修正...")
            
            # 从LLM返回的名称/理由中提取关键词
            fallback_keywords = [
                result["main_quota"].get("name", ""),
                result["main_quota"].get("reason", ""),
                user_input
            ]
            volume = result["main_quota"].get("volume", volume_hint)
            
            corrected = local_search_by_keywords(fallback_keywords, volume, top_k=10)
            
            if corrected:
                print(f"  ✅ 已修正！找到 {len(corrected)} 条本地库真实定额\n")
                result["main_quota"] = {
                    "code": corrected[0].get("quota_no"),
                    "name": corrected[0].get("name"),
                    "volume": corrected[0].get("volume"),
                    "chapter": corrected[0].get("chapter"),
                    "unit": corrected[0].get("unit"),
                    "base_price": corrected[0].get("base_price"),
                    "reason": "本地库验证修正"
                }
                result["verified_results"] = corrected
                result["original_fake_code"] = code
                result["verification_status"] = "corrected"
                
                print("=" * 60)
                print("语义匹配结果（已自动修正 ✅）")
                print("=" * 60)
                print(f"\n【主定额】（修正后）")
                mq = result["main_quota"]
                print(f"  定额编号：{mq.get('code', 'N/A')}")
                print(f"  定额名称：{mq.get('name', 'N/A')}")
                print(f"  基价：{mq.get('base_price', 'N/A')} 元")
                print(f"  章节：{mq.get('chapter', 'N/A')}")
                print(f"\n  ⚠️ 原LLM编号 [{code}] 已被替换")
            else:
                result["verification_status"] = "unverified"
                print(f"  ❌ 本地库也未找到匹配，请人工确认")
                print(f"\n【原始LLM结果】（⚠️ 未验证）")
                mq = result["main_quota"]
                print(f"  定额编号：{mq.get('code', 'N/A')}（可能不存在！）")
                print(f"  定额名称：{mq.get('name', 'N/A')}")
        
        # 辅定额同样验证
        if "auxiliary_quotas" in result and result["auxiliary_quotas"]:
            verified_aux = []
            for aq in result["auxiliary_quotas"]:
                aux_code = aq.get("code", "")
                aux_check = verify_quota_code(aux_code)
                if aux_check["exists"]:
                    aq["base_price"] = aux_check["data"].get("base_price")
                    aq["chapter"] = aux_check["data"].get("chapter")
                    aq["verified"] = True
                    verified_aux.append(aq)
                else:
                    aq["verified"] = False
                    aq["warning"] = f"编号 {aux_code} 在本地库中不存在"
                    verified_aux.append(aq)
            
            result["auxiliary_quotas"] = verified_aux
            
            print(f"\n【辅定额】")
            for i, aq in enumerate(result["auxiliary_quotas"], 1):
                status = "✅" if aq.get("verified") else "⚠️不存在"
                print(f"  {i}. {aq.get('code', 'N/A')} - {aq.get('name', 'N/A')} {status}")
                if aq.get("base_price"):
                    print(f"     基价:{aq['base_price']}元")
                if aq.get("warning"):
                    print(f"     ⚠️ {aq['warning']}")
        
        if "main_materials" in result and result["main_materials"]:
            print(f"\n【主材】")
            for m in result["main_materials"]:
                print(f"  - {m.get('name', 'N/A')} {m.get('spec', '')} (损耗率:{m.get('loss_rate', 0)*100:.1f}%)")
        
        print(f"\n置信度：{result.get('confidence', 0)*100:.0f}%")
        print("=" * 60)
        
        return result
    
    return result


# ============================================================
# 命令行入口
# ============================================================

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python llm_semantic_match.py \"工作内容描述\" [分册提示]")
        print("示例：python llm_semantic_match.py \"热泵安装\" \"第2册热力设备\"")
        print()
        print("搜索模式：")
        print("  (默认)      # LLM语义匹配 + 本地验证")
        print("  --hybrid    # 混合搜索（LLM提取关键词 + 本地库搜索）")
        print()
        print("模型切换：")
        print("  --hunyuan  # 腾讯混元（默认，免费）")
        print("  --doubao   # 豆包（备选）")
        print()
        print("环境变量：")
        print("  LLM_PROVIDER=hunyuan|doubao   # 模型选择")
        print("  HUNYUAN_API_KEY=sk-xxx        # 混元API Key（OpenAI兼容，推荐）")
        print("  HUNYUAN_SECRET_ID/KEY=xxx     # 混元密钥（SDK方式，备选）")
        print("  DOUBAO_API_KEY=xxx            # 豆包API Key")
        print("  DOUBAO_ENDPOINT_ID=ep-xxx     # 豆包接入点ID（可选）")
        sys.exit(1)

    user_input = sys.argv[1]
    volume_hint = sys.argv[2] if len(sys.argv) > 2 else ""

    # 支持命令行指定模型
    if "--doubao" in sys.argv:
        use_doubao()
    elif "--hunyuan" in sys.argv:
        use_hunyuan()

    # 混合搜索模式
    if "--hybrid" in sys.argv:
        result = hybrid_search(user_input, volume_hint)
    else:
        result = semantic_match(user_input, volume_hint)

    # 如果需要JSON输出（供程序调用）
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
