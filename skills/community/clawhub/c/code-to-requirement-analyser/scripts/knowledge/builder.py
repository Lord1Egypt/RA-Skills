# scripts/knowledge/builder.py
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class KnowledgeNode:
    id: str
    type: str
    title: str
    content: Dict[str, Any]
    trade_dimension: Dict[str, List[str]]
    source: Dict[str, Any]
    tags: List[str]
    embeddings: Optional[List[float]] = None  # 用于语义检索
    
@dataclass
class KnowledgeEdge:
    source: str
    target: str
    relation_type: str  # similar/upstream/downstream/contains/conflicts
    strength: float
    metadata: Dict[str, Any]

class KnowledgeGraphBuilder:
    """知识图谱构建器"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.nodes_path = self.base_path / "nodes"
        self.edges_path = self.base_path / "edges"
        self.index_path = self.base_path / "index.json"
        
        self.nodes_path.mkdir(parents=True, exist_ok=True)
        self.edges_path.mkdir(parents=True, exist_ok=True)
        
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """加载索引"""
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "nodes": {},  # id -> metadata
            "tags": {},   # tag -> [node_ids]
            "dimensions": {},  # dimension -> [node_ids]
            "last_updated": None
        }
    
    def add_knowledge(self, analysis_result: Dict, source_file: str) -> KnowledgeNode:
        """添加知识节点"""
        # 生成唯一ID
        content_hash = self._hash_content(analysis_result)
        node_id = f"KNOW-{datetime.now().strftime('%Y%m%d')}-{content_hash[:8]}"
        
        # 创建节点
        dimension = analysis_result.get("trade_dimension", {})
        node = KnowledgeNode(
            id=node_id,
            type="trade_requirement",
            title=self._generate_title(dimension),
            content={
                "functional_requirements": analysis_result.get("functional_requirements", []),
                "business_rules": analysis_result.get("business_rules", []),
                "data_dictionary": analysis_result.get("data_dictionary", []),
                "business_process": analysis_result.get("business_process", {}),
                "confidence": analysis_result.get("analysis_confidence", {}),
                "suggestions": analysis_result.get("suggestions", [])
            },
            trade_dimension=dimension,
            source={
                "file": source_file,
                "extracted_at": datetime.now().isoformat(),
                "extractor_version": "2.0.0"
            },
            tags=self._generate_tags(dimension, analysis_result)
        )
        
        # 保存节点
        node_file = self.nodes_path / f"{node_id}.json"
        with open(node_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(node), f, ensure_ascii=False, indent=2)
        
        # 更新索引
        self._update_index(node)
        
        # 建立关联
        edges = self._establish_relationships(node)
        
        return node, edges
    
    def _hash_content(self, content: Dict) -> str:
        """内容哈希"""
        content_str = json.dumps(content, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def _generate_title(self, dimension: Dict) -> str:
        """生成标题"""
        parts = []
        if dimension.get("trade_type") and dimension["trade_type"][0] != "未识别":
            parts.append(dimension["trade_type"][0])
        if dimension.get("product_type"):
            parts.append(dimension["product_type"][0])
        if dimension.get("lifecycle") and dimension["lifecycle"][0] != "未识别":
            parts.append(dimension["lifecycle"][0])
        
        return "".join(parts) + "业务需求" if parts else "交易业务需求"
    
    def _generate_tags(self, dimension: Dict, analysis: Dict) -> List[str]:
        """生成标签"""
        tags = set()
        
        # 维度标签
        tags.update(dimension.get("lifecycle", []))
        tags.update(dimension.get("trade_type", []))
        tags.update(dimension.get("product_type", []))
        tags.update(dimension.get("channel", []))
        
        # 功能标签
        for req in analysis.get("functional_requirements", [])[:3]:
            tags.add(req.get("name", "")[:10])
        
        # 技术标签
        components = analysis.get("components", [])
        if any("el-" in str(c) for c in components):
            tags.add("ElementUI")
        if any("a-" in str(c) for c in components):
            tags.add("AntDesign")
        
        return list(tags)[:15]  # 限制数量
    
    def _update_index(self, node: KnowledgeNode):
        """更新索引"""
        self.index["nodes"][node.id] = {
            "title": node.title,
            "type": node.type,
            "created_at": node.source["extracted_at"],
            "tags": node.tags[:5]
        }
        
        # 标签索引
        for tag in node.tags:
            if tag not in self.index["tags"]:
                self.index["tags"][tag] = []
            if node.id not in self.index["tags"][tag]:
                self.index["tags"][tag].append(node.id)
        
        # 维度索引
        dim_key = f"{','.join(node.trade_dimension.get('trade_type', []))}_" \
                 f"{','.join(node.trade_dimension.get('lifecycle', []))}"
        if dim_key not in self.index["dimensions"]:
            self.index["dimensions"][dim_key] = []
        self.index["dimensions"][dim_key].append(node.id)
        
        self.index["last_updated"] = datetime.now().isoformat()
        self._save_index()
    
    def _save_index(self):
        """保存索引"""
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _establish_relationships(self, new_node: KnowledgeNode) -> List[KnowledgeEdge]:
        """建立知识关联"""
        edges = []
        
        # 与最近节点比较相似度
        recent_nodes = list(self.index["nodes"].keys())[-20:]
        
        for existing_id in recent_nodes:
            if existing_id == new_node.id:
                continue
            
            existing_file = self.nodes_path / f"{existing_id}.json"
            if not existing_file.exists():
                continue
            
            with open(existing_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            
            # 计算相似度
            similarity = self._calculate_similarity(new_node, existing)
            
            if similarity > 0.6:
                # 确定关系类型
                relation_type = self._determine_relation_type(
                    new_node.trade_dimension, 
                    existing.get("trade_dimension", {})
                )
                
                edge = KnowledgeEdge(
                    source=new_node.id,
                    target=existing_id,
                    relation_type=relation_type,
                    strength=round(similarity, 2),
                    metadata={"calculated_at": datetime.now().isoformat()}
                )
                
                # 保存边
                edge_file = self.edges_path / f"{new_node.id}_{existing_id}.json"
                with open(edge_file, 'w', encoding='utf-8') as f:
                    json.dump(asdict(edge), f, ensure_ascii=False, indent=2)
                
                edges.append(edge)
        
        return edges
    
    def _calculate_similarity(self, node1: KnowledgeNode, node2: Dict) -> float:
        """计算节点相似度（简化版）"""
        score = 0.0
        total = 0.0
        
        # 维度匹配
        dim1 = node1.trade_dimension
        dim2 = node2.get("trade_dimension", {})
        
        for key in ["trade_type", "lifecycle", "product_type"]:
            set1 = set(dim1.get(key, []))
            set2 = set(dim2.get(key, []))
            if set1 and set2:
                intersection = len(set1 & set2)
                union = len(set1 | set2)
                if union > 0:
                    score += (intersection / union) * 0.3
                    total += 0.3
        
        # 标签匹配
        tags1 = set(node1.tags)
        tags2 = set(node2.get("tags", []))
        if tags1 and tags2:
            score += len(tags1 & tags2) / max(len(tags1), len(tags2)) * 0.3
            total += 0.3
        
        # 功能需求匹配
        func1 = json.dumps(node1.content.get("functional_requirements", []))
        func2 = json.dumps(node2.get("content", {}).get("functional_requirements", []))
        if func1 and func2:
            # 简单的字符串相似度
            common = len(set(func1.split()) & set(func2.split()))
            total_words = max(len(set(func1.split())), len(set(func2.split())))
            if total_words > 0:
                score += (common / total_words) * 0.4
                total += 0.4
        
        return score / total if total > 0 else 0.0
    
    def _determine_relation_type(self, dim1: Dict, dim2: Dict) -> str:
        """确定关系类型"""
        # 检查上下游（生命周期顺序）
        lifecycle_order = ["创建", "审核", "执行", "确认", "清算", "结算", "归档"]
        
        life1 = dim1.get("lifecycle", [""])[0] if dim1.get("lifecycle") else ""
        life2 = dim2.get("lifecycle", [""])[0] if dim2.get("lifecycle") else ""
        
        if life1 and life2:
            idx1 = lifecycle_order.index(life1) if life1 in lifecycle_order else -1
            idx2 = lifecycle_order.index(life2) if life2 in lifecycle_order else -1
            
            if idx1 >= 0 and idx2 >= 0:
                if idx1 < idx2:
                    return "upstream"  # node1在node2之前
                elif idx1 > idx2:
                    return "downstream"  # node1在node2之后
        
        # 检查冲突（相同维度但不同规则）
        type1 = set(dim1.get("trade_type", []))
        type2 = set(dim2.get("trade_type", []))
        if type1 & type2:  # 有共同类型
            return "similar"
        
        return "related"
    
    def search(self, query: Dict) -> List[Dict]:
        """搜索知识"""
        results = []
        
        # 标签搜索
        if "tags" in query:
            for tag in query["tags"]:
                node_ids = self.index["tags"].get(tag, [])
                for node_id in node_ids:
                    if node_id not in [r["id"] for r in results]:
                        node_file = self.nodes_path / f"{node_id}.json"
                        if node_file.exists():
                            with open(node_file, 'r', encoding='utf-8') as f:
                                results.append(json.load(f))
        
        # 维度搜索
        if "dimension" in query:
            dim_key = f"{query['dimension'].get('trade_type', '')}_" \
                     f"{query['dimension'].get('lifecycle', '')}"
            node_ids = self.index["dimensions"].get(dim_key, [])
            for node_id in node_ids:
                if node_id not in [r["id"] for r in results]:
                    node_file = self.nodes_path / f"{node_id}.json"
                    if node_file.exists():
                        with open(node_file, 'r', encoding='utf-8') as f:
                            results.append(json.load(f))
        
        return results
    
    def get_related_knowledge(self, node_id: str, relation_type: Optional[str] = None) -> List[Dict]:
        """获取关联知识"""
        related = []
        
        # 查找所有相关的边
        for edge_file in self.edges_path.glob(f"{node_id}_*.json"):
            with open(edge_file, 'r', encoding='utf-8') as f:
                edge = json.load(f)
            
            if relation_type is None or edge.get("relation_type") == relation_type:
                target_id = edge.get("target")
                target_file = self.nodes_path / f"{target_id}.json"
                if target_file.exists():
                    with open(target_file, 'r', encoding='utf-8') as f:
                        node = json.load(f)
                        node["relation"] = edge
                        related.append(node)
        
        return related