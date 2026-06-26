#!/usr/bin/env python3
"""
Ancientman-CN 主压缩器 - 增强版
支持：英文术语映射、时态保留、可逆解压缩、流式处理
"""

import re
import json
from typing import Dict, List, Optional, Generator, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class CompressionMode(Enum):
    """压缩模式"""
    LITE = "lite"           # 轻度
    STANDARD = "standard"   # 标准
    ULTRA = "ultra"         # 极致
    CLASSICAL = "classical" # 古风


@dataclass
class CompressionResult:
    """压缩结果"""
    original: str
    compressed: str
    original_length: int
    compressed_length: int
    reduction_percent: float
    mode: str
    mapping_log: List[Tuple[str, str]] = None  # 记录映射关系用于解压缩
    
    def __post_init__(self):
        if self.mapping_log is None:
            self.mapping_log = []


class AncientmanCompressor:
    """
    增强版古代人压缩器
    支持功能：
    - 英文技术术语缩写映射
    - 时态标记智能保留
    - 可逆解压缩
    - 流式处理
    """
    
    # ==================== 词汇映射表 ====================
    
    # 英文技术术语缩写映射 (新增)
    EN_TECH_ABBR = {
        # 开发框架
        "Kubernetes": "k8s",
        "PostgreSQL": "pg",
        "JavaScript": "JS",
        "TypeScript": "TS",
        "Docker": "dock",
        "Configuration": "cfg",
        "Application": "app",
        "Server": "srv",
        "Client": "cli",
        "Database": "DB",
        "Connection": "conn",
        "Authentication": "auth",
        "Authorization": "authz",
        "Environment": "env",
        "Variable": "var",
        "Function": "fn",
        "Object": "obj",
        "Array": "arr",
        "String": "str",
        "Integer": "int",
        "Boolean": "bool",
        "Repository": "repo",
        "Package": "pkg",
        "Interface": "iface",
        "Abstract": "abs",
        "Implementation": "impl",
        "Exception": "ex",
        "Runtime": "rt",
        "Compile": "cmp",
        "Debug": "dbg",
        "Release": "rel",
        "Version": "ver",
        "Dependency": "dep",
        "Platform": "plat",
        "Service": "svc",
        "Message": "msg",
        "Request": "req",
        "Response": "resp",
        "Parameter": "param",
        "Attribute": "attr",
        "Component": "comp",
        "Container": "cont",
        "Image": "img",
        "Volume": "vol",
        "Network": "net",
        "Protocol": "prot",
        "Header": "hdr",
        "Payload": "pld",
        "Token": "tok",
        "Credential": "cred",
        "Secret": "sec",
        "Certificate": "cert",
        "Encryption": "enc",
        "Decryption": "dec",
        "Hash": "hs",
        "Signature": "sig",
        "Validation": "val",
        "Verification": "vrf",
        "Transformation": "xform",
    }
    
    # 中文技术术语映射
    CN_TECH_MAP = {
        # 高频技术词
        "数据库": "库",
        "服务器": "服",
        "网络": "网",
        "配置": "配",
        "错误": "错",
        "问题": "问",
        "解决方案": "解",
        "性能": "性",
        "内存": "存",
        "缓存": "缓",
        "日志": "志",
        "代码": "码",
        "函数": "函",
        "变量": "变",
        "数组": "组",
        "对象": "对",
        "接口": "口",
        "协议": "议",
        "请求": "请",
        "响应": "应",
        "数据": "数",
        "文件": "件",
        "系统": "系",
        "程序": "程",
        "应用": "用",
        "软件": "软",
        "硬件": "硬",
        "设备": "设",
        "资源": "资",
        "权限": "权",
        "用户": "户",
        "连接": "连",
        "状态": "态",
        "时间": "时",
        "空间": "空",
        "速度": "速",
        "容量": "量",
        "频率": "频",
        "温度": "温",
        "压力": "压",
        "版本": "版",
        
        # 操作动词
        "检查": "检",
        "测试": "测",
        "验证": "验",
        "修复": "修",
        "优化": "优",
        "部署": "部",
        "启动": "启",
        "停止": "停",
        "断开": "断",
        "上传": "上",
        "下载": "下",
        "安装": "安",
        "卸载": "卸",
        "创建": "建",
        "删除": "删",
        "修改": "改",
        "复制": "复",
        "移动": "移",
        "搜索": "搜",
        "排序": "排",
        "过滤": "滤",
        "加密": "密",
        "解密": "解",
        "分析": "析",
        "设计": "设",
        "开发": "开",
        "发布": "发",
        "更新": "更",
        "备份": "备",
        "恢复": "恢",
        "监控": "监",
        "报警": "警",
        "统计": "统",
        "计算": "算",
        "处理": "处",
        "存储": "储",
        "传输": "输",
        "接收": "收",
        "发送": "发",
        "打印": "印",
        "扫描": "扫",
        "读取": "读",
        "写入": "写",
        "执行": "执",
        "完成": "完",
        "失败": "败",
        "成功": "成",
        "等待": "等",
        "超时": "超",
        "重试": "重",
        "返回": "返",
    }
    
    # 文言虚词映射
    CLASSICAL_MAP = {
        "因为": "盖",
        "由于": "盖",
        "所以": "故",
        "因此": "故",
        "于是": "故",
        "如果": "若",
        "假如": "若",
        "要是": "若",
        "那么": "则",
        "然后": "后",
        "之后": "后",
        "之前": "前",
        "之中": "中",
        "之内": "内",
        "之外": "外",
        "之上": "上",
        "之下": "下",
        "应该": "宜",
        "应当": "宜",
        "必须": "须",
        "需要": "需",
        "可以": "可",
        "能够": "能",
        "但是": "然",
        "然而": "然",
        "不过": "然",
        "可是": "然",
        "并且": "",
        "而且": "",
        "或者": "或",
        "还是": "",
        "对于": "于",
        "关于": "于",
    }
    
    # 需要保留的关键词（不压缩）
    PRESERVE_KEYWORDS = [
        # API和协议
        "API", "HTTP", "HTTPS", "JSON", "XML", "SQL", "NoSQL", "REST", "GraphQL",
        "WebSocket", "TCP", "UDP", "DNS", "CDN", "SSL", "TLS", "SSH", "FTP",
        # 前端框架
        "React", "Vue", "Angular", "Svelte", "Next.js", "Nuxt.js",
        # 后端框架
        "Node.js", "Express", "FastAPI", "Django", "Flask", "Spring",
        "Rails", "Laravel", "Gin", "Echo",
        # 编程语言
        "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C++",
        "C#", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",
        # 工具和服务
        "Docker", "Kubernetes", "k8s", "Git", "GitHub", "GitLab", "Nginx",
        # 数据库
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra",
        "DynamoDB", "InfluxDB", "TimescaleDB",
        # 云服务
        "AWS", "Azure", "GCP", "阿里云", "腾讯云", "阿里云", "华为云",
        # React Hooks
        "useMemo", "useEffect", "useState", "useCallback", "useRef",
        "useContext", "useReducer", "useLayoutEffect", "useImperativeHandle",
        # 操作系统
        "Windows", "Linux", "macOS", "iOS", "Android", "Chrome",
        "Firefox", "Safari", "Edge", "Ubuntu", "CentOS", "Debian",
        # 其他技术
        "CI/CD", "DevOps", "Microservice", "Serverless", "Container",
        "Kubernetes", "Helm", "Prometheus", "Grafana", "Kibana",
        "Grafana", "Prometheus", "Jaeger", "Zipkin",
    ]
    
    # 时态标记（用于智能保留）
    TENSE_MARKERS = ["已", "了", "过", "着", "正", "将", "会", "能", "可"]
    
    # 需要删除的填充词
    FILLER_WORDS = [
        "好的", "好的", "没问题", "明白了", "当然", "确实", "的确",
        "其实", "实际上", "基本上", "大概", "可能", "也许",
        "请", "麻烦", "您好", "你好", "谢谢", "感谢", "抱歉",
        "对不起", "不好意思", "请问", "请教", "帮忙", "帮助", "协助",
    ]
    
    # ==================== 初始化 ====================
    
    def __init__(self, mode: CompressionMode = CompressionMode.STANDARD, preserve_tense: bool = True):
        """
        初始化压缩器
        
        Args:
            mode: 压缩模式
            preserve_tense: 是否保留时态标记
        """
        self.mode = mode
        self.preserve_tense = preserve_tense
        self._mapping_log: List[Tuple[str, str]] = []
        
    def reset_log(self):
        """重置映射日志"""
        self._mapping_log = []
    
    # ==================== 核心压缩方法 ====================
    
    def compress(self, text: str) -> CompressionResult:
        """
        压缩文本
        
        Args:
            text: 原始文本
            
        Returns:
            CompressionResult: 压缩结果
        """
        if not text:
            return CompressionResult(
                original=text,
                compressed="",
                original_length=0,
                compressed_length=0,
                reduction_percent=0,
                mode=self.mode.value
            )
        
        self.reset_log()
        original = text
        compressed = text
        
        # 1. 保护关键词
        compressed = self._protect_keywords(compressed)
        
        # 2. 根据模式应用压缩
        if self.mode == CompressionMode.LITE:
            compressed = self._compress_lite(compressed)
        elif self.mode == CompressionMode.STANDARD:
            compressed = self._compress_standard(compressed)
        elif self.mode == CompressionMode.ULTRA:
            compressed = self._compress_ultra(compressed)
        elif self.mode == CompressionMode.CLASSICAL:
            compressed = self._compress_classical(compressed)
        
        # 3. 恢复关键词
        compressed = self._restore_keywords(compressed)
        
        # 计算结果
        orig_len = len(original.replace(' ', ''))
        comp_len = len(compressed.replace(' ', ''))
        reduction = (orig_len - comp_len) / orig_len * 100 if orig_len > 0 else 0
        
        return CompressionResult(
            original=original,
            compressed=compressed,
            original_length=len(original),
            compressed_length=len(compressed),
            reduction_percent=round(reduction, 1),
            mode=self.mode.value,
            mapping_log=self._mapping_log.copy()
        )
    
    def compress_stream(self, text: str, buffer_size: int = 50) -> Generator[str, None, None]:
        """
        流式压缩文本
        
        Args:
            text: 原始文本
            buffer_size: 缓冲区大小（字符数）
            
        Yields:
            str: 压缩后的文本片段
        """
        if not text:
            yield ""
            return
        
        buffer = ""
        
        # 按句子或缓冲区大小分割
        sentences = re.split(r'([。！？；\n])', text)
        
        for i, part in enumerate(sentences):
            if i % 2 == 0:  # 句子内容
                buffer += part
                if len(buffer) >= buffer_size:
                    result = self.compress(buffer)
                    yield result.compressed
                    buffer = ""
            else:  # 标点
                buffer += part
                if len(buffer) >= buffer_size:
                    result = self.compress(buffer)
                    yield result.compressed
                    buffer = ""
        
        # 处理剩余内容
        if buffer:
            result = self.compress(buffer)
            yield result.compressed
    
    def decompress(self, compressed: str, mapping_log: List[Tuple[str, str]] = None) -> str:
        """
        解压缩（尝试恢复原始文本）
        
        注意：这是尽力而为的恢复，不保证100%准确
        
        Args:
            compressed: 压缩后的文本
            mapping_log: 映射日志（如果有的话）
            
        Returns:
            str: 尽量恢复后的文本
        """
        if not compressed:
            return ""
        
        result = compressed
        
        # 如果有映射日志，尝试逆向恢复
        if mapping_log:
            # 按反向顺序恢复（先短后长）
            sorted_log = sorted(mapping_log, key=lambda x: len(x[1]), reverse=False)
            for short, original in sorted_log:
                result = result.replace(short, original)
        
        # 尝试用内置映射表恢复（启发式）
        result = self._try_restore(result)
        
        return result
    
    # ==================== 内部压缩方法 ====================
    
    def _protect_keywords(self, text: str) -> str:
        """保护关键词"""
        result = text
        for keyword in self.PRESERVE_KEYWORDS:
            placeholder = f"__PKW_{hash(keyword) % 10000}__"
            result = result.replace(keyword, placeholder)
            result = result.replace(keyword.lower(), placeholder)
            result = result.replace(keyword.upper(), placeholder)
        return result
    
    def _restore_keywords(self, text: str) -> str:
        """恢复关键词"""
        result = text
        for keyword in self.PRESERVE_KEYWORDS:
            placeholder = f"__PKW_{hash(keyword) % 10000}__"
            result = result.replace(placeholder, keyword)
        return result
    
    def _log_mapping(self, original: str, compressed: str):
        """记录映射关系"""
        if original != compressed:
            self._mapping_log.append((compressed, original))
    
    def _compress_lite(self, text: str) -> str:
        """轻度压缩"""
        result = text
        
        # 删除填充词
        for word in self.FILLER_WORDS:
            result = result.replace(word, "")
        
        # 删除多余空格
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip()
    
    def _compress_standard(self, text: str) -> str:
        """标准压缩"""
        result = text
        
        # 删除填充词
        for word in self.FILLER_WORDS:
            result = result.replace(word, "")
        
        # 应用中文映射
        for original, replacement in sorted(self.CN_TECH_MAP.items(), key=lambda x: len(x[0]), reverse=True):
            new_result = result.replace(original, replacement)
            if new_result != result:
                self._log_mapping(original, replacement)
            result = new_result
        
        # 删除虚词
        result = re.sub(r'[的地得]', '', result)
        
        # 删除多余空格
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip()
    
    def _compress_ultra(self, text: str) -> str:
        """极致压缩"""
        result = text
        
        # 英文术语缩写
        for original, replacement in self.EN_TECH_ABBR.items():
            new_result = result.replace(original, replacement)
            if new_result != result:
                self._log_mapping(original, replacement)
            result = new_result
        
        # 中文术语映射
        for original, replacement in sorted(self.CN_TECH_MAP.items(), key=lambda x: len(x[0]), reverse=True):
            new_result = result.replace(original, replacement)
            if new_result != result:
                self._log_mapping(original, replacement)
            result = new_result
        
        # 删除虚词
        result = re.sub(r'[的地得了着过在是和或与及以及并且或者还是]', '', result)
        
        # 符号代替连接词
        result = re.sub(r'(导致|引起|造成|使得|致使)', '→', result)
        
        # 极度精简
        result = re.sub(r'[吧呢啊呀啦嘛哇哦哟]', '', result)
        result = re.sub(r'[，。；！？、：；""''（）《》【】]', ' ', result)
        
        # 删除多余空格
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip()
    
    def _compress_classical(self, text: str) -> str:
        """古风压缩"""
        result = text
        
        # 英文术语缩写
        for original, replacement in self.EN_TECH_ABBR.items():
            new_result = result.replace(original, replacement)
            if new_result != result:
                self._log_mapping(original, replacement)
            result = new_result
        
        # 中文术语映射
        for original, replacement in sorted(self.CN_TECH_MAP.items(), key=lambda x: len(x[0]), reverse=True):
            new_result = result.replace(original, replacement)
            if new_result != result:
                self._log_mapping(original, replacement)
            result = new_result
        
        # 文言虚词映射
        for original, replacement in sorted(self.CLASSICAL_MAP.items(), key=lambda x: len(x[0]), reverse=True):
            new_result = result.replace(original, replacement)
            if new_result != result:
                self._log_mapping(original, replacement)
            result = new_result
        
        # 时态保留逻辑
        if self.preserve_tense:
            # 保留"已"、"了"、"过"与动词的组合
            result = re.sub(r'([\u4e00-\u9fa5])已([\u4e00-\u9fa5]+)', r'\1已\2', result)
            result = re.sub(r'([\u4e00-\u9fa5])了([\u4e00-\u9fa5]+)', r'\1了\2', result)
        else:
            # 删除大部分虚词
            result = re.sub(r'[的了着过]', '', result)
        
        # 删除其他虚词
        result = re.sub(r'[的地得在是和或与及以及并且或者还是]', '', result)
        
        # 符号代替连接词
        result = re.sub(r'(因为|由于|所以|因此|于是|导致|引起|造成)', '→', result)
        
        # 删除标点和语气词
        result = re.sub(r'[吧呢啊呀啦嘛哇哦哟。，、；！？、：；""''（）《》【】]', '', result)
        
        # 删除多余空格
        result = re.sub(r'\s+', '', result)
        
        return result.strip()
    
    def _try_restore(self, text: str) -> str:
        """尝试恢复压缩的文本（启发式）"""
        result = text
        
        # 反向恢复中文术语
        reverse_map = {v: k for k, v in self.CN_TECH_MAP.items()}
        for short, original in sorted(reverse_map.items(), key=lambda x: len(x[0]), reverse=True):
            # 只有当短词是独立词时才替换
            result = re.sub(rf'(?<!\w){re.escape(short)}(?!\w)', original, result)
        
        # 反向恢复文言虚词
        reverse_classical = {v: k for k, v in self.CLASSICAL_MAP.items() if v}
        for short, original in sorted(reverse_classical.items(), key=lambda x: len(x[0]), reverse=True):
            result = result.replace(short, original)
        
        # 恢复连接词
        result = result.replace('→', '导致')
        
        return result
    
    # ==================== 辅助方法 ====================
    
    def demo(self, text: str) -> Dict:
        """
        演示所有模式的压缩效果对比
        
        Args:
            text: 测试文本
            
        Returns:
            Dict: 各模式压缩效果对比
        """
        modes = [
            ("轻度模式", CompressionMode.LITE),
            ("标准模式", CompressionMode.STANDARD),
            ("极致模式", CompressionMode.ULTRA),
            ("古风模式", CompressionMode.CLASSICAL),
        ]
        
        results = {
            "original": text,
            "original_length": len(text),
            "modes": []
        }
        
        for mode_name, mode in modes:
            old_mode = self.mode
            self.mode = mode
            result = self.compress(text)
            results["modes"].append({
                "mode": mode_name,
                "compressed": result.compressed,
                "length": result.compressed_length,
                "reduction_percent": result.reduction_percent,
                "saved_chars": result.original_length - result.compressed_length
            })
            self.mode = old_mode
        
        return results
    
    def export_mappings(self) -> Dict:
        """导出映射表"""
        return {
            "en_tech_abbr": self.EN_TECH_ABBR,
            "cn_tech_map": self.CN_TECH_MAP,
            "classical_map": self.CLASSICAL_MAP,
            "preserve_keywords": self.PRESERVE_KEYWORDS,
        }
    
    def import_mappings(self, mappings: Dict):
        """导入自定义映射"""
        if "en_tech_abbr" in mappings:
            self.EN_TECH_ABBR.update(mappings["en_tech_abbr"])
        if "cn_tech_map" in mappings:
            self.CN_TECH_MAP.update(mappings["cn_tech_map"])
        if "classical_map" in mappings:
            self.CLASSICAL_MAP.update(mappings["classical_map"])


# ==================== LangChain 集成 ====================

class AncientmanCompressionHandler:
    """
    LangChain 压缩回调处理器
    用于在 LangChain 的 LLM 调用中自动压缩输入/输出
    """
    
    def __init__(self, mode: str = "standard", preserve_tense: bool = True):
        """
        初始化处理器
        
        Args:
            mode: 压缩模式 (lite/standard/ultra/classical)
            preserve_tense: 是否保留时态
        """
        mode_map = {
            "lite": CompressionMode.LITE,
            "standard": CompressionMode.STANDARD,
            "ultra": CompressionMode.ULTRA,
            "classical": CompressionMode.CLASSICAL,
        }
        self.mode = mode_map.get(mode, CompressionMode.STANDARD)
        self.preserve_tense = preserve_tense
        self.compressor = AncientmanCompressor(self.mode, self.preserve_tense)
    
    def compress_input(self, text: str) -> str:
        """压缩输入文本"""
        result = self.compressor.compress(text)
        return result.compressed
    
    def decompress_output(self, text: str) -> str:
        """解压缩输出文本"""
        return self.compressor.decompress(text)


class AncientmanDocumentTransformer:
    """
    LangChain 文档转换器
    用于批量压缩文档
    """
    
    def __init__(self, mode: str = "standard", preserve_tense: bool = True):
        self.mode = mode
        self.preserve_tense = preserve_tense
        mode_map = {
            "lite": CompressionMode.LITE,
            "standard": CompressionMode.STANDARD,
            "ultra": CompressionMode.ULTRA,
            "classical": CompressionMode.CLASSICAL,
        }
        self.compressor = AncientmanCompressor(mode_map.get(mode, CompressionMode.STANDARD), preserve_tense)
    
    def transform_documents(self, documents: List[str]) -> List[Dict]:
        """
        批量转换文档
        
        Args:
            documents: 文档列表
            
        Returns:
            List[Dict]: 转换后的文档列表
        """
        results = []
        for doc in documents:
            result = self.compressor.compress(doc)
            results.append({
                "original": doc,
                "compressed": result.compressed,
                "reduction_percent": result.reduction_percent,
                "mapping_log": result.mapping_log,
            })
        return results


# ==================== CLI 工具 ====================

def main():
    """命令行入口"""
    import sys
    
    compressor = AncientmanCompressor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo" and len(sys.argv) > 2:
            # 演示模式
            text = " ".join(sys.argv[2:])
            results = compressor.demo(text)
            
            print("=" * 70)
            print(f"原始文本 ({results['original_length']}字符):")
            print(results['original'])
            print("=" * 70)
            
            for mode_result in results['modes']:
                print(f"\n【{mode_result['mode']}】")
                print(f"压缩后: {mode_result['compressed']}")
                print(f"节省: {mode_result['reduction_percent']}% ({mode_result['saved_chars']}字符)")
            
        elif sys.argv[1] == "--export":
            # 导出映射表
            import json
            print(json.dumps(compressor.export_mappings(), ensure_ascii=False, indent=2))
            
        elif sys.argv[1] in ["--help", "-h"]:
            print("""
Ancientman-CN 增强版压缩器

用法:
    python ancientman_enhanced.py [选项] [文本]

选项:
    --demo <文本>    演示所有模式的压缩效果
    --export        导出映射表
    --help, -h      显示帮助

示例:
    python ancientman_enhanced.py --demo "数据库连接失败，请检查网络配置"
    python ancientman_enhanced.py "服务器宕机需要重启"
""")
        else:
            # 直接压缩
            text = " ".join(sys.argv[1:])
            result = compressor.compress(text)
            print(result.compressed)
    else:
        # 交互模式
        print("Ancientman-CN 增强版 (输入文本压缩, quit退出)")
        while True:
            try:
                text = input("\n> ")
                if text.lower() in ["quit", "exit", "q"]:
                    break
                result = compressor.compress(text)
                print(f"  → {result.compressed}")
                print(f"  节省: {result.reduction_percent}%")
            except EOFError:
                break


if __name__ == "__main__":
    main()
