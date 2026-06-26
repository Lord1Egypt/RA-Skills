# scripts/parser/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import ast
import re
import hashlib
import json
from pathlib import Path
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ParsedComponent:
    name: str
    type: str  # form/table/chart/action
    props: Dict[str, Any]
    events: List[str]
    children: List['ParsedComponent']
    source_range: tuple  # (start_line, end_line)
    business_semantic: Optional[str] = None  # 推断的业务语义


@dataclass
class ParsedAPI:
    method: str
    endpoint: str
    params: Dict[str, Any]
    response_handler: Optional[str]
    business_purpose: Optional[str] = None


@dataclass
class ParsedRule:
    rule_type: str  # validation/permission/calculation/flow
    expression: str
    source: str  # 原始代码片段
    confidence: float  # 0-1
    business_meaning: Optional[str] = None


class CacheManager:
    """文件指纹缓存管理器"""
    
    def __init__(self, cache_dir: str = "~/.openclaw/cache/trade-analyzer/"):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "cache_metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """加载缓存元数据"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载缓存元数据失败: {e}")
        return {"entries": {}, "version": "2.1.0"}
    
    def _save_metadata(self):
        """保存缓存元数据"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存缓存元数据失败: {e}")
    
    def _calc_file_hash(self, file_path: str) -> str:
        """计算文件内容的 SHA256 哈希"""
        try:
            content = Path(file_path).read_bytes()
            return hashlib.sha256(content).hexdigest()
        except Exception as e:
            logger.error(f"计算文件哈希失败: {e}")
            return ""
    
    def get_cached_result(self, file_path: str) -> Optional[Dict]:
        """获取缓存的分析结果"""
        try:
            file_path = str(Path(file_path).resolve())
            current_hash = self._calc_file_hash(file_path)
            
            if not current_hash:
                return None
            
            entry = self.metadata["entries"].get(file_path)
            if not entry:
                return None
            
            # 检查文件是否已更改
            if entry.get("hash") != current_hash:
                logger.info(f"文件已更改，跳过缓存: {file_path}")
                return None
            
            # 检查缓存是否过期（默认 7 天）
            cache_time = datetime.fromisoformat(entry.get("timestamp", "2000-01-01"))
            if (datetime.now() - cache_time).days > 7:
                logger.info(f"缓存已过期: {file_path}")
                return None
            
            # 加载缓存文件
            cache_file = self.cache_dir / f"{entry['cache_id']}.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    logger.info(f"命中缓存: {file_path}")
                    return json.load(f)
        
        except Exception as e:
            logger.warning(f"读取缓存失败: {e}")
        
        return None
    
    def save_result(self, file_path: str, result: Dict) -> bool:
        """保存分析结果到缓存"""
        try:
            file_path = str(Path(file_path).resolve())
            file_hash = self._calc_file_hash(file_path)
            
            if not file_hash:
                return False
            
            # 生成缓存 ID
            cache_id = f"cache_{file_hash[:16]}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cache_file = self.cache_dir / f"{cache_id}.json"
            
            # 保存结果
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            # 更新元数据
            self.metadata["entries"][file_path] = {
                "hash": file_hash,
                "timestamp": datetime.now().isoformat(),
                "cache_id": cache_id,
                "file_name": Path(file_path).name
            }
            
            # 清理旧缓存（保留最近 100 个）
            self._cleanup_old_cache()
            
            self._save_metadata()
            logger.info(f"缓存已保存: {file_path}")
            return True
        
        except Exception as e:
            logger.warning(f"保存缓存失败: {e}")
            return False
    
    def _cleanup_old_cache(self, max_entries: int = 100):
        """清理旧缓存条目"""
        entries = self.metadata["entries"]
        if len(entries) <= max_entries:
            return
        
        # 按时间排序，保留最新的
        sorted_entries = sorted(
            entries.items(),
            key=lambda x: x[1].get("timestamp", ""),
            reverse=True
        )
        
        # 删除旧条目
        to_remove = sorted_entries[max_entries:]
        for file_path, entry in to_remove:
            cache_file = self.cache_dir / f"{entry['cache_id']}.json"
            try:
                if cache_file.exists():
                    cache_file.unlink()
            except Exception:
                pass
            del entries[file_path]
        
        logger.info(f"清理了 {len(to_remove)} 个旧缓存条目")
    
    def clear_cache(self):
        """清除所有缓存"""
        try:
            # 删除所有缓存文件
            for cache_file in self.cache_dir.glob("cache_*.json"):
                cache_file.unlink()
            
            # 重置元数据
            self.metadata = {"entries": {}, "version": "2.1.0"}
            self._save_metadata()
            
            logger.info("缓存已清除")
            return True
        except Exception as e:
            logger.error(f"清除缓存失败: {e}")
            return False
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计信息"""
        entries = self.metadata.get("entries", {})
        total_size = sum(
            (self.cache_dir / f"{entry['cache_id']}.json").stat().st_size
            for entry in entries.values()
            if (self.cache_dir / f"{entry['cache_id']}.json").exists()
        )
        
        return {
            "total_entries": len(entries),
            "cache_dir": str(self.cache_dir),
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "version": self.metadata.get("version", "unknown")
        }


class BaseCodeParser(ABC):
    """代码解析器抽象基类"""
    
    def __init__(self, file_path: str, use_cache: bool = True):
        self.file_path = file_path
        self.use_cache = use_cache
        self.cache_manager = CacheManager() if use_cache else None
        self.content = self._read_file()
        self.ast = None
        
    def _read_file(self) -> str:
        """读取文件内容，支持自动编码检测"""
        try:
            # 尝试检测编码
            import chardet
            raw = Path(self.file_path).read_bytes()
            detected = chardet.detect(raw)
            encoding = detected.get('encoding') or 'utf-8'
            confidence = detected.get('confidence', 0)
            
            logger.debug(f"检测到编码: {encoding} (置信度: {confidence:.2%})")
            
            # 使用检测到的编码解码
            return raw.decode(encoding, errors='replace')
        
        except ImportError:
            # 如果没有 chardet，使用默认 UTF-8
            logger.debug("chardet 未安装，使用默认 UTF-8 编码")
            try:
                return Path(self.file_path).read_text(encoding='utf-8')
            except UnicodeDecodeError:
                # 如果 UTF-8 失败，尝试 GBK
                logger.debug("UTF-8 解码失败，尝试 GBK")
                return Path(self.file_path).read_text(encoding='gbk', errors='replace')
        
        except Exception as e:
            logger.error(f"读取文件失败 {self.file_path}: {e}")
            raise
    
    def parse_with_cache(self) -> Dict[str, Any]:
        """带缓存的解析入口"""
        # 尝试从缓存读取
        if self.cache_manager:
            cached = self.cache_manager.get_cached_result(self.file_path)
            if cached is not None:
                cached["_from_cache"] = True
                cached["_cache_hit"] = True
                return cached
        
        # 执行解析
        result = self.parse()
        result["_from_cache"] = False
        result["_cache_hit"] = False
        
        # 保存到缓存
        if self.cache_manager:
            self.cache_manager.save_result(self.file_path, result)
        
        return result
    
    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """主解析入口"""
        pass
    
    @abstractmethod
    def extract_components(self) -> List[ParsedComponent]:
        """提取UI组件"""
        pass
    
    @abstractmethod
    def extract_apis(self) -> List[ParsedAPI]:
        """提取API调用"""
        pass
    
    @abstractmethod
    def extract_business_rules(self) -> List[ParsedRule]:
        """提取业务规则"""
        pass
    
    def calculate_complexity(self) -> Dict[str, int]:
        """计算代码复杂度指标"""
        try:
            return {
                "lines_of_code": len(self.content.splitlines()),
                "cyclomatic_complexity": self._calc_cyclomatic(),
                "component_count": len(self.extract_components()),
                "api_count": len(self.extract_apis())
            }
        except Exception as e:
            logger.warning(f"计算复杂度失败: {e}")
            return {
                "lines_of_code": len(self.content.splitlines()),
                "cyclomatic_complexity": 0,
                "component_count": 0,
                "api_count": 0
            }
    
    def _calc_cyclomatic(self) -> int:
        """计算圈复杂度"""
        try:
            # 简化实现：统计if/for/while/switch/catch
            patterns = [r'\bif\b', r'\bfor\b', r'\bwhile\b', 
                       r'\bswitch\b', r'\bcatch\b', r'\?.*:']
            count = sum(len(re.findall(p, self.content)) for p in patterns)
            return count + 1
        except Exception as e:
            logger.warning(f"计算圈复杂度失败: {e}")
            return 1
    
    def _safe_regex_search(self, pattern: str, text: str, flags: int = 0, 
                          default=None, context: str = "") -> Any:
        """安全的正则搜索，带错误处理"""
        try:
            return re.search(pattern, text, flags)
        except re.error as e:
            logger.warning(f"正则表达式错误 [{context}]: {e}")
            return default
        except Exception as e:
            logger.warning(f"正则搜索失败 [{context}]: {e}")
            return default
    
    def _safe_regex_findall(self, pattern: str, text: str, flags: int = 0,
                           context: str = "") -> List:
        """安全的正则查找所有，带错误处理"""
        try:
            return re.findall(pattern, text, flags)
        except re.error as e:
            logger.warning(f"正则表达式错误 [{context}]: {e}")
            return []
        except Exception as e:
            logger.warning(f"正则查找失败 [{context}]: {e}")
            return []
    
    def _safe_regex_finditer(self, pattern: str, text: str, flags: int = 0,
                            context: str = ""):
        """安全的正则迭代查找，带错误处理"""
        try:
            return re.finditer(pattern, text, flags)
        except re.error as e:
            logger.warning(f"正则表达式错误 [{context}]: {e}")
            return iter([])
        except Exception as e:
            logger.warning(f"正则迭代失败 [{context}]: {e}")
            return iter([])
