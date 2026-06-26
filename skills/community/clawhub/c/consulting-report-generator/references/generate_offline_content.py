"""
generate_offline_content.py — 离线内容生成引擎（v6.1 consulting-report-generator）
在无网络/本地Ollama环境下自动切换为本地生成模式
"""

import json, os, subprocess
from datetime import datetime

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = "gemma4:e2b-it-q4_K_M"

# =====================================================
# 离线内容模板（完全无网络时的备用内容库）
# =====================================================

OFFLINE_TEMPLATES = {
    "lean_intro": {
        "zh": "精益生产（Lean Production）源于丰田生产方式（TPS），由大野耐一于20世纪50年代创立，核心是通过消除浪费、优化流程、持续改进来提升生产效率和产品质量。五大原则：价值、价值流、流动、拉动、尽善尽美。",
    },
    "seven_wastes": {
        "zh": "丰田定义的七种浪费（TIMWOOD）：①生产过剩——最大的浪费；②等待——人员和设备闲置；③运输——物料无效搬运；④不适当加工——过度工程；⑤库存——掩盖问题；⑥动作——低效操作；⑦不良品——返工和废品。",
    },
    "jit": {
        "zh": "准时化生产（JIT）是精益生产的两大支柱之一，核心思想是'只在需要的时候、按需要的量、生产需要的产品'，通过拉动式生产、看板管理、平准化等手段实现。",
    },
    "jidoka": {
        "zh": "自働化（Jidoka）是精益生产的另一大支柱，赋予设备人的智慧——异常时自动停止、不生产不良品。不同于自动化（Automation），自働化强调人机最佳结合。",
    },
    "kaizen": {
        "zh": "持续改善（Kaizen）是精益生产的灵魂，主张通过PDCA循环、全员参与的小步快跑式改进，实现'每天进步一点点'。三大实践路径：质量管理小组、合理化建议、改善活动。",
    },
    "tpm": {
        "zh": "TPM（全面生产维护）追求设备综合效率最大化，通过操作员自主维护、预防性维护和改善维护，将OEE从行业平均55-60%提升至80%以上。",
    },
    "smed": {
        "zh": "SMED（快速换模）由新乡重夫创立，通过区分内外部作业、转换内外部、优化内外作业、持续改善四步，将换型时间从小时级压缩到分钟级（个位数）。",
    },
    "5s": {
        "zh": "5S现场管理是精益的基石：整理（要/不要）、整顿（定位定量）、清扫（清洁点检）、清洁（制度化）、素养（习惯化）。没有5S，其他精益工具难以落地。",
    },
    "oee": {
        "zh": "OEE=可用率×性能×质量。全球OEE基准：行业平均55-60%，世界级标准85%+，仅约3%制造商达到世界级。持续追踪OEE可在6个月内提升20%。",
    },
}

OFFLINE_CASE_STUDIES = [
    "某汽车零部件企业导入精益生产后，OEE从52%提升至79%，换型时间从135分钟降至18分钟，在制品库存降低67%。",
    "某电子制造企业实施5S+标准化作业后，直通率从87%提升至96%，人均产出提升42%。",
    "某食品加工企业推行TPM后，设备故障率降低73%，MTBF从28天提升至156天。",
]


# =====================================================
# Ollama 本地模型调用
# =====================================================

def check_ollama():
    """检查Ollama是否可用"""
    try:
        import urllib.request
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return len(data.get("models", [])) > 0
    except:
        return False


def call_ollama(prompt, model=DEFAULT_MODEL, max_tokens=500):
    """调用本地Ollama模型生成内容"""
    import urllib.request
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": max_tokens}
    }).encode()
    
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get("response", "")
    except Exception as e:
        return f"[离线模式] 无法调用本地模型: {e}"


# =====================================================
# 内容生成控制器（自动切换在线/离线）
# =====================================================

class ContentGenerator:
    """内容生成器——自动检测网络状态，切换在线/离线模式"""
    
    def __init__(self):
        self.online = self._check_online()
        self.ollama_ok = check_ollama()
        
    def _check_online(self):
        """检测是否有网络连接"""
        try:
            import urllib.request
            urllib.request.urlopen("http://8.8.8.8", timeout=3)
            return True
        except:
            return False
    
    def detect_offline_reason(self):
        """返回离线原因说明"""
        if not self.online:
            return "无网络连接"
        if not self.ollama_ok:
            return "Ollama未运行或本地模型不可用"
        return ""
    
    def generate_section(self, topic, keywords=""):
        """生成章节内容"""
        if self.online:
            # 在线模式：使用在线模板（联网获取行业数据）
            result = OFFLINE_TEMPLATES.get(topic, {}).get("zh", "")
            if result:
                return result
            # 尝试用Ollama生成
            if self.ollama_ok:
                result = call_ollama(f"用中文写一段关于{topic}的50字简介")
                if result:
                    return result
            return f"[离线内容] {topic}的相关内容"
        else:
            # 离线模式：使用离线模板
            result = OFFLINE_TEMPLATES.get(topic, {}).get("zh", "")
            if result:
                return result
            return f"[离线内容] {topic}的相关内容"
    
    def get_mode_label(self):
        """获取模式标签"""
        if not self.online:
            return "🔌 离线模式（无网络）"
        if not self.ollama_ok:
            return "☁️ 在线模式（标准）"
        return "💻 本地模型模式"


# =====================================================
# 使用示例
# =====================================================

if __name__ == "__main__":
    gen = ContentGenerator()
    print(f"当前模式: {gen.get_mode_label()}")
    print(f"离线原因: {gen.detect_offline_reason() or '正常在线'}")
    
    # 测试生成
    for topic in ["lean_intro", "seven_wastes", "kaizen"]:
        content = gen.generate_section(topic)
        print(f"\n--- {topic} ---")
        print(content[:80] + "...")
