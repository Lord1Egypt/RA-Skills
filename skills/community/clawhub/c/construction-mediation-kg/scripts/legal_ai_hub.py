# 法律AI多后端集成框架
# 度量衡商事调解智库 - 统一AI接口层
# 支持：通义法睿、智谱AI、智合AI（预留）

import os
import json
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any

# ============================================================
# 抽象基类
# ============================================================

class LegalAIProvider(ABC):
    """法律AI服务抽象基类"""
    
    @abstractmethod
    def legal_search(self, issue: str) -> Dict[str, Any]:
        """法律检索"""
        pass
    
    @abstractmethod
    def analyze_case(self, description: str) -> Dict[str, Any]:
        """案件分析"""
        pass
    
    @abstractmethod
    def draft_document(self, doc_type: str, case_info: Dict) -> Dict[str, Any]:
        """文书生成"""
        pass
    
    @abstractmethod
    def calculate_risk(self, factors: List[str]) -> Dict[str, Any]:
        """风险评估"""
        pass

# ============================================================
# 通义法睿实现
# ============================================================

class FaruiProvider(LegalAIProvider):
    """阿里云通义法睿"""
    
    SYSTEM_PROMPT = """你是一位专业的建设工程商事调解助手，擅长处理工程款纠纷、工期争议、
质量争议、变更签证争议等案件。你的目标是帮助调解员分析案件、梳理争议焦点、
提供法律建议和调解方案。"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.model = "farui-plus"
        
    def _call_api(self, prompt: str, system_prompt: Optional[str] = None) -> Dict:
        """统一API调用"""
        try:
            import dashscope
            dashscope.api_key = self.api_key
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = dashscope.Generation.call(
                model=self.model,
                messages=messages,
                result_format="message",
                max_tokens=2000
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "content": response.output.choices[0].message.content,
                    "provider": "通义法睿"
                }
            return {"success": False, "error": response.message}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def legal_search(self, issue: str) -> Dict[str, Any]:
        prompt = f"""请检索以下法律问题的相关依据：{issue}
请提供：1.相关法律条文 2.司法解释 3.裁判案例要点"""
        return self._call_api(prompt, self.SYSTEM_PROMPT + "\n擅长法律检索")
    
    def analyze_case(self, description: str) -> Dict[str, Any]:
        prompt = f"""请分析以下案件，识别：1.争议焦点 2.法律关系 3.关键证据
案件：{description}"""
        return self._call_api(prompt, self.SYSTEM_PROMPT)
    
    def draft_document(self, doc_type: str, case_info: Dict) -> Dict[str, Any]:
        prompt = f"请生成{doc_type}。案件信息：{json.dumps(case_info, ensure_ascii=False)}"
        return self._call_api(prompt, self.SYSTEM_PROMPT + "\n擅长法律文书写作")
    
    def calculate_risk(self, factors: List[str]) -> Dict[str, Any]:
        prompt = f"评估风险：{chr(10).join(factors)}。提供：风险等级、分析、建议"
        return self._call_api(prompt, self.SYSTEM_PROMPT + "\n擅长法律风险评估")


# ============================================================
# 智谱AI (GLM) 实现
# ============================================================

class ZhipuAIProvider(LegalAIProvider):
    """智谱AI GLM系列"""
    
    SYSTEM_PROMPT = """你是一位专业的建设工程法律顾问，擅长工程合同、造价纠纷、
商事调解领域。请用专业、严谨的方式回答问题。"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        self.model = "glm-4"
        
    def _call_api(self, prompt: str, system_prompt: Optional[str] = None) -> Dict:
        try:
            import dashscope
            dashscope.api_key = self.api_key
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = dashscope.Generation.call(
                model=self.model,
                messages=messages,
                result_format="message"
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "content": response.output.choices[0].message.content,
                    "provider": "智谱AI-GLM4"
                }
            return {"success": False, "error": response.message}
        except ImportError:
            return {"success": False, "error": "请安装dashscope: pip install dashscope"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def legal_search(self, issue: str) -> Dict[str, Any]:
        prompt = f"""作为建设工程法律专家，请检索：{issue}
要求：引用具体法条、说明实务要点"""
        return self._call_api(prompt, self.SYSTEM_PROMPT)
    
    def analyze_case(self, description: str) -> Dict[str, Any]:
        prompt = f"""作为建设工程纠纷专家，分析：{description}
输出：争议焦点、法律分析、调解建议"""
        return self._call_api(prompt, self.SYSTEM_PROMPT)
    
    def draft_document(self, doc_type: str, case_info: Dict) -> Dict[str, Any]:
        prompt = f"生成{doc_type}：{json.dumps(case_info, ensure_ascii=False)}"
        return self._call_api(prompt, self.SYSTEM_PROMPT)
    
    def calculate_risk(self, factors: List[str]) -> Dict[str, Any]:
        prompt = f"法律风险评估：{chr(10).join(factors)}"
        return self._call_api(prompt, self.SYSTEM_PROMPT)


# ============================================================
# 智合AI预留接口（待开放）
# ============================================================

class ZhiheAIProvider(LegalAIProvider):
    """
    智合AI预留接口
    状态：智合AI当前为SaaS平台，API接口暂未开放
    预留原因：等待官方开放API后接入
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.status = "pending"  # pending / available
        self.note = "智合AI当前仅支持Web/App使用，API接口pending开放"
    
    def legal_search(self, issue: str) -> Dict[str, Any]:
        return {
            "success": False,
            "error": self.note,
            "provider": "智合AI",
            "status": "waiting_api"
        }
    
    def analyze_case(self, description: str) -> Dict[str, Any]:
        return {
            "success": False,
            "error": self.note,
            "provider": "智合AI",
            "status": "waiting_api"
        }
    
    def draft_document(self, doc_type: str, case_info: Dict) -> Dict[str, Any]:
        return {
            "success": False,
            "error": self.note,
            "provider": "智合AI",
            "status": "waiting_api"
        }
    
    def calculate_risk(self, factors: List[str]) -> Dict[str, Any]:
        return {
            "success": False,
            "error": self.note,
            "provider": "智合AI",
            "status": "waiting_api"
        }


# ============================================================
# 统一入口
# ============================================================

class LegalAIHub:
    """
    法律AI统一入口
    自动选择可用provider，支持降级切换
    """
    
    PROVIDERS = {
        "farui": FaruiProvider,
        "zhipu": ZhipuAIProvider,
        "zhihe": ZhiheAIProvider
    }
    
    def __init__(self, preferred: str = "farui"):
        """
        初始化
        
        Args:
            preferred: 首选provider (farui/zhipu/zhihe)
        """
        self.primary = preferred
        self._init_providers()
    
    def _init_providers(self):
        """初始化所有provider"""
        self.providers = {}
        for name, cls in self.PROVIDERS.items():
            try:
                self.providers[name] = cls()
            except:
                pass
    
    def _get_provider(self, name: Optional[str] = None):
        """获取可用provider"""
        preferred = name or self.primary
        if preferred in self.providers:
            return self.providers[preferred]
        # 降级遍历
        for name in ["farui", "zhipu", "zhihe"]:
            if name in self.providers:
                return self.providers[name]
        return None
    
    def search(self, issue: str, provider: Optional[str] = None) -> str:
        """法律检索"""
        p = self._get_provider(provider)
        if p:
            result = p.legal_search(issue)
            if result.get("success"):
                return result["content"]
            return f"错误：{result.get('error')}"
        return "无可用AI服务"
    
    def analyze(self, description: str, provider: Optional[str] = None) -> str:
        """案件分析"""
        p = self._get_provider(provider)
        if p:
            result = p.analyze_case(description)
            if result.get("success"):
                return result["content"]
            return f"错误：{result.get('error')}"
        return "无可用AI服务"
    
    def draft(self, doc_type: str, case_info: Dict, provider: Optional[str] = None) -> str:
        """文书生成"""
        p = self._get_provider(provider)
        if p:
            result = p.draft_document(doc_type, case_info)
            if result.get("success"):
                return result["content"]
            return f"错误：{result.get('error')}"
        return "无可用AI服务"
    
    def risk(self, factors: List[str], provider: Optional[str] = None) -> str:
        """风险评估"""
        p = self._get_provider(provider)
        if p:
            result = p.calculate_risk(factors)
            if result.get("success"):
                return result["content"]
            return f"错误：{result.get('error')}"
        return "无可用AI服务"
    
    def status(self) -> Dict:
        """查看所有provider状态"""
        status = {}
        for name, p in self.PROVIDERS.items():
            try:
                status[name] = "available" if name in self.providers else "no_key"
            except:
                status[name] = "error"
            if name == "zhihe":
                status[name] = "pending"  # 强制标记pending
        return status


# ============================================================
# 便捷函数
# ============================================================

def legal_search(issue: str, provider: str = "auto") -> str:
    """快速法律检索"""
    hub = LegalAIHub()
    return hub.search(issue, provider if provider != "auto" else None)

def case_analysis(description: str, provider: str = "auto") -> str:
    """快速案件分析"""
    hub = LegalAIHub()
    return hub.analyze(description, provider if provider != "auto" else None)


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    # 检查可用provider
    hub = LegalAIHub()
    print("Provider状态:", hub.status())
    
    # 设置API Key
    # os.environ["DASHSCOPE_API_KEY"] = "your-key"
    # os.environ["ZHIPU_API_KEY"] = "your-key"
    
    # 使用示例
    # result = legal_search("工程款优先受偿权的行使条件")
    # print(result)
    
    print("\n法律AI集成框架已加载")
    print("设置环境变量后即可使用：")
    print("  - DASHSCOPE_API_KEY (通义法睿)")
    print("  - ZHIPU_API_KEY (智谱AI)")
    print("  - 智合AI pending，待API开放")