# 通义法睿API集成模块
# 度量衡商事调解智库 - 法律AI增强组件
# 基于阿里云百炼平台 farui-plus 模型

import os
import json
from typing import Optional, Dict, List, Any

# ============================================================
# 配置管理
# ============================================================

class FaruiConfig:
    """通义法睿配置管理"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化配置
        
        Args:
            api_key: 阿里云百炼API Key，默认从环境变量读取
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.model = "farui-plus"
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
    def validate(self) -> bool:
        """验证配置是否有效"""
        return bool(self.api_key)

# ============================================================
# 核心API调用
# ============================================================

class FaruiClient:
    """通义法睿API客户端"""
    
    def __init__(self, config: Optional[FaruiConfig] = None):
        self.config = config or FaruiConfig()
        
    def _prepare_messages(self, user_input: str, system_prompt: Optional[str] = None) -> List[Dict]:
        """准备消息格式"""
        messages = []
        if system_prompt:
            messages.append({
                "role": "system", 
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": user_input
        })
        return messages
    
    def call(self, 
             user_input: str,
             system_prompt: Optional[str] = None,
             max_tokens: int = 2000,
             temperature: float = 0.7,
             stream: bool = False) -> Dict[str, Any]:
        """
        调用通义法睿API
        
        Args:
            user_input: 用户输入内容
            system_prompt: 系统提示词
            max_tokens: 最大生成token数
            temperature: 温度参数
            stream: 是否流式输出
            
        Returns:
            API响应结果
        """
        if not self.config.validate():
            return {
                "success": False,
                "error": "请配置 DASHSCOPE_API_KEY 环境变量"
            }
        
        try:
            import dashscope
            dashscope.api_key = self.config.api_key
            
            messages = self._prepare_messages(user_input, system_prompt)
            
            response = dashscope.Generation.call(
                model=self.config.model,
                messages=messages,
                result_format="message",
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "content": response.output.choices[0].message.content,
                    "usage": response.usage,
                    "request_id": response.request_id
                }
            else:
                return {
                    "success": False,
                    "error": response.code,
                    "message": response.message
                }
                
        except ImportError:
            return {
                "success": False,
                "error": "请安装 dashscope: pip install dashscope"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# ============================================================
# 商事调解专用场景封装
# ============================================================

class MediationFarui:
    """商事调解场景的通义法睿封装"""
    
    SYSTEM_PROMPT = """你是一位专业的建设工程商事调解助手，擅长处理工程款纠纷、工期争议、
质量争议、变更签证争议等案件。你的目标是帮助调解员分析案件、梳理争议焦点、
提供法律建议和调解方案。"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = FaruiClient(FaruiConfig(api_key))
        
    def analyze_case(self, case_description: str) -> Dict[str, Any]:
        """
        案件分析：分析案件事实，梳理争议焦点
        
        Args:
            case_description: 案件描述文本
            
        Returns:
            分析结果
        """
        prompt = f"""请分析以下建设工程调解案件，识别：
1. 争议焦点（工程款金额、工期延误责任、质量缺陷认定、变更签证有效性等）
2. 涉及的法律关系（合同关系、侵权关系、合作关系等）
3. 关键证据（合同、签证、验收报告、往来函件等）

案件材料：
{case_description}

请以结构化方式输出分析结果。"""
        
        return self.client.call(
            user_input=prompt,
            system_prompt=self.SYSTEM_PROMPT
        )
    
    def legal_search(self, legal_issue: str) -> Dict[str, Any]:
        """
        法律检索：检索相关法律法规和司法解释
        
        Args:
            legal_issue: 法律问题描述
            
        Returns:
            检索结果
        """
        prompt = f"""请检索以下法律问题的相关依据：
{legal_issue}

请提供：
1. 相关法律条文（《民法典》《建筑法》等）
2. 司法解释和指导意见
3. 相关裁判案例（简要说明）
4. 实务中的裁判观点"""
        
        return self.client.call(
            user_input=prompt,
            system_prompt=self.SYSTEM_PROMPT + "\n你擅长法律检索和案例分析。"
        )
    
    def draft_document(self, doc_type: str, case_info: Dict) -> Dict[str, Any]:
        """
        文书生成：根据案件信息生成法律文书
        
        Args:
            doc_type: 文书类型（调解申请书、答辩状、调解协议等）
            case_info: 案件信息字典
            
        Returns:
            生成的文书内容
        """
        prompt = f"""请生成{doc_type}。

案件信息：
{json.dumps(case_info, ensure_ascii=False, indent=2)}

请按照法律文书格式规范生成，内容完整、准确、符合法律规定。"""
        
        return self.client.call(
            user_input=prompt,
            system_prompt=self.SYSTEM_PROMPT + "\n你擅长法律文书写作。"
        )
    
    def calculate_legal_risk(self, risk_factors: List[str]) -> Dict[str, Any]:
        """
        法律风险评估：评估调解方案的法律风险
        
        Args:
            risk_factors: 风险因素列表
            
        Returns:
            风险评估结果
        """
        prompt = f"""请评估以下调解方案的法律风险：

风险因素：
{chr(10).join(['- ' + r for r in risk_factors])}

请提供：
1. 风险等级（高/中/低）
2. 具体风险分析
3. 风险防范建议
4. 可能的法律后果"""
        
        return self.client.call(
            user_input=prompt,
            system_prompt=self.SYSTEM_PROMPT + "\n你擅长法律风险评估和防范。"
        )


# ============================================================
# 便捷函数
# ============================================================

def quick_legal_search(issue: str, api_key: Optional[str] = None) -> str:
    """
    快速法律检索（单函数调用）
    
    Args:
        issue: 法律问题
        api_key: API Key
        
    Returns:
        检索结果文本
    """
    mediator = MediationFarui(api_key)
    result = mediator.legal_search(issue)
    if result.get("success"):
        return result["content"]
    return f"错误：{result.get('error')}"


def quick_case_analysis(description: str, api_key: Optional[str] = None) -> str:
    """
    快速案件分析（单函数调用）
    
    Args:
        description: 案件描述
        api_key: API Key
        
    Returns:
        分析结果文本
    """
    mediator = MediationFarui(api_key)
    result = mediator.analyze_case(description)
    if result.get("success"):
        return result["content"]
    return f"错误：{result.get('error')}"


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    # 示例：快速法律检索
    # 设置API Key: os.environ["DASHSCOPE_API_KEY"] = "your-api-key"
    
    # 示例1：法律检索
    # result = quick_legal_search("建设工程合同无效的法律后果")
    # print(result)
    
    # 示例2：案件分析
    # result = quick_case_analysis("发包人拖欠工程款，承包人主张违约金")
    # print(result)
    
    # 示例3：完整使用
    # mediator = MediationFarui()
    # result = mediator.legal_search("工程款优先受偿权的行使条件")
    # print(result)
    
    print("通义法睿集成模块已加载")
    print("使用方法：")
    print("1. 设置环境变量: os.environ['DASHSCOPE_API_KEY'] = 'your-key'")
    print("2. from farui_integration import quick_legal_search, quick_case_analysis")
    print("3. 调用相应函数进行法律检索或案件分析")