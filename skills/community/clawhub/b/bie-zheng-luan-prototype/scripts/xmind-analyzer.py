#!/usr/bin/env python3
"""
XMind文件分析器
用于分析产品功能脑图、信息架构等XMind文件
提取思维导图节点和层级关系，转换为结构化数据
"""

import sys
import json
import zipfile
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import xml.etree.ElementTree as ET

@dataclass
class XMindNode:
    """XMind节点"""
    id: str
    title: str
    level: int
    parent_id: Optional[str]
    children: List['XMindNode']
    attributes: Dict[str, Any]  # 额外属性：颜色、图标、备注等

@dataclass
class XMindAnalysisResult:
    """XMind分析结果"""
    file_path: str
    title: str                    # 主标题
    root_topic: XMindNode         # 根节点
    all_topics: List[XMindNode]   # 所有节点（扁平化）
    structure_type: str           # 结构类型：logical, tree, spreadsheet等
    statistics: Dict[str, int]    # 统计信息
    modules: List[Dict[str, Any]] # 推断的功能模块
    pages: List[Dict[str, Any]]   # 推断的页面结构
    features: List[Dict[str, Any]] # 推断的功能点

class XMindAnalyzer:
    """XMind文件分析器"""

    def __init__(self, xmind_path: str):
        self.xmind_path = xmind_path
        self.zip_file = None
        self.content = None

    def load_xmind(self) -> bool:
        """加载XMind文件"""
        try:
            self.zip_file = zipfile.ZipFile(self.xmind_path, 'r')
            return True
        except Exception as e:
            print(f"加载XMind文件失败: {e}")
            return False

    def extract_content(self) -> bool:
        """提取XMind内容"""
        if not self.zip_file:
            return False

        try:
            # XMind文件结构
            # - content.xml (XMind 8格式)
            # - content.json (XMind 2020+格式)
            # - manifest.xml

            # 尝试读取JSON格式（新版本）
            if 'content.json' in self.zip_file.namelist():
                content_json = self.zip_file.read('content.json').decode('utf-8')
                self.content = json.loads(content_json)
                return True

            # 尝试读取XML格式（旧版本）
            if 'content.xml' in self.zip_file.namelist():
                content_xml = self.zip_file.read('content.xml').decode('utf-8')
                self.content = self._parse_xml_content(content_xml)
                return True

            # 某些XMind版本使用其他命名
            for name in self.zip_file.namelist():
                if name.endswith('.json') and 'content' in name:
                    content_json = self.zip_file.read(name).decode('utf-8')
                    self.content = json.loads(content_json)
                    return True
                if name.endswith('.xml') and 'content' in name:
                    content_xml = self.zip_file.read(name).decode('utf-8')
                    self.content = self._parse_xml_content(content_xml)
                    return True

            print("未找到有效的XMind内容文件")
            return False

        except Exception as e:
            print(f"解析XMind内容失败: {e}")
            return False

    def _parse_xml_content(self, xml_content: str) -> Dict[str, Any]:
        """解析XML格式的XMind内容"""
        root = ET.fromstring(xml_content)
        result = {}

        # XMind XML结构：
        # <xmap-content>
        #   <sheet>
        #     <topic id="root" central="true">
        #       <title>...</title>
        #       <children>
        #         <topics type="attached">
        #           <topic id="...">
        #             ...

        sheets = []
        for sheet in root.findall('.//sheet') or root.findall('.//Sheet'):
            sheet_data = {
                'id': sheet.get('id', ''),
                'title': ''
            }

            # 查找根主题
            root_topic = sheet.find('.//topic[@central="true"]') or \
                         sheet.find('.//Topic[@central="true"]') or \
                         sheet.find('.//topic') or \
                         sheet.find('.//Topic')

            if root_topic:
                sheet_data['rootTopic'] = self._parse_xml_topic(root_topic)
                title_elem = root_topic.find('title') or root_topic.find('Title')
                if title_elem:
                    sheet_data['title'] = title_elem.text or ''

            sheets.append(sheet_data)

        result['sheets'] = sheets
        return result

    def _parse_xml_topic(self, topic_elem: ET.Element, parent_id: str = None, level: int = 0) -> Dict[str, Any]:
        """解析XML格式的主题节点"""
        topic_id = topic_elem.get('id', '')

        # 获取标题
        title_elem = topic_elem.find('title') or topic_elem.find('Title')
        title = title_elem.text if title_elem is not None else ''

        topic_data = {
            'id': topic_id,
            'title': title,
            'level': level,
            'parent_id': parent_id,
            'children': [],
            'attributes': {}
        }

        # 解析子节点
        children_elem = topic_elem.find('children') or topic_elem.find('Children')
        if children_elem:
            for topics_type in ['attached', 'detached']:
                topics_elem = children_elem.find(f'topics[@type="{topics_type}"]') or \
                              children_elem.find(f'Topics[@type="{topics_type}"]')
                if topics_elem:
                    for child_topic in topics_elem.findall('topic') or topics_elem.findall('Topic'):
                        child_data = self._parse_xml_topic(child_topic, topic_id, level + 1)
                        topic_data['children'].append(child_data)

        # 解析额外属性
        # 颜色
        color_elem = topic_elem.find('.//color') or topic_elem.find('.//Color')
        if color_elem:
            topic_data['attributes']['color'] = color_elem.get('value', '')

        # 图标
        marker_ref_elem = topic_elem.find('.//marker-ref') or topic_elem.find('.//MarkerRef')
        if marker_ref_elem:
            topic_data['attributes']['marker_id'] = marker_ref_elem.get('marker-id', '')

        # 备注
        notes_elem = topic_elem.find('.//notes') or topic_elem.find('.//Notes')
        if notes_elem:
            notes_text = notes_elem.find('text') or notes_elem.find('Text')
            if notes_text:
                topic_data['attributes']['notes'] = notes_text.text

        return topic_data

    def analyze(self) -> XMindAnalysisResult:
        """分析XMind文件"""
        if not self.load_xmind():
            return None

        if not self.extract_content():
            return None

        # 解析内容
        root_topic, all_topics = self._parse_topics()

        # 统计信息
        statistics = self._calculate_statistics(all_topics)

        # 推断功能模块、页面、功能点
        modules, pages, features = self._infer_structure(root_topic, all_topics)

        # 确定结构类型
        structure_type = self._determine_structure(root_topic)

        return XMindAnalysisResult(
            file_path=self.xmind_path,
            title=root_topic.title if root_topic else "",
            root_topic=root_topic,
            all_topics=all_topics,
            structure_type=structure_type,
            statistics=statistics,
            modules=modules,
            pages=pages,
            features=features
        )

    def _parse_topics(self) -> tuple:
        """解析所有主题节点"""
        root_topic = None
        all_topics = []

        if not self.content:
            return root_topic, all_topics

        # 处理JSON格式
        if 'sheets' in self.content:
            for sheet in self.content['sheets']:
                if 'rootTopic' in sheet:
                    root_topic = self._parse_json_topic(sheet['rootTopic'], None, 0)
                    all_topics = self._flatten_topics(root_topic)

        return root_topic, all_topics

    def _parse_json_topic(self, topic_data: Dict[str, Any], parent_id: str = None, level: int = 0) -> XMindNode:
        """解析JSON格式的主题节点"""
        topic_id = topic_data.get('id', '')
        title = topic_data.get('title', '')

        # 解析子节点
        children = []
        if 'children' in topic_data:
            for child in topic_data['children'].get('attached', []):
                child_node = self._parse_json_topic(child, topic_id, level + 1)
                children.append(child_node)

        # 解析额外属性
        attributes = {}
        if 'labels' in topic_data:
            attributes['labels'] = topic_data['labels']
        if 'note' in topic_data:
            attributes['note'] = topic_data['note']
        if 'image' in topic_data:
            attributes['image'] = topic_data['image']
        if 'marker' in topic_data:
            attributes['marker'] = topic_data['marker']
        if 'style' in topic_data:
            attributes['style'] = topic_data['style']
        if 'color' in topic_data:
            attributes['color'] = topic_data['color']

        return XMindNode(
            id=topic_id,
            title=title,
            level=level,
            parent_id=parent_id,
            children=children,
            attributes=attributes
        )

    def _flatten_topics(self, topic: XMindNode) -> List[XMindNode]:
        """扁平化所有主题节点"""
        topics = [topic]
        for child in topic.children:
            topics.extend(self._flatten_topics(child))
        return topics

    def _calculate_statistics(self, topics: List[XMindNode]) -> Dict[str, int]:
        """计算统计信息"""
        stats = {
            'total_topics': len(topics),
            'max_depth': 0,
            'topics_by_level': {}
        }

        for topic in topics:
            stats['max_depth'] = max(stats['max_depth'], topic.level)
            stats['topics_by_level'][topic.level] = stats['topics_by_level'].get(topic.level, 0) + 1

        return stats

    def _infer_structure(self, root_topic: XMindNode, all_topics: List[XMindNode]) -> tuple:
        """推断功能模块、页面和功能点"""
        modules = []
        pages = []
        features = []

        if not root_topic:
            return modules, pages, features

        # 帺于节点标题推断类型
        # 常见的命名模式：
        # - 模块命名：包含"模块"、"管理"、"系统"等
        # - 页面命名：包含"页面"、"列表"、"详情"等
        # - 功能命名：包含"功能"、"操作"、"按钮"等

        module_keywords = ['模块', '管理', '系统', 'module', 'manage', 'system']
        page_keywords = ['页面', '列表', '详情', 'page', 'list', 'detail', 'view']
        feature_keywords = ['功能', '操作', '按钮', 'function', 'action', 'feature', 'button']

        for topic in all_topics:
            title_lower = topic.title.lower()

            # 推断模块
            if any(kw in title_lower for kw in module_keywords):
                modules.append({
                    'id': topic.id,
                    'name': topic.title,
                    'level': topic.level,
                    'children_count': len(topic.children),
                    'children': [child.title for child in topic.children[:10]]  # 最多显示10个
                })

            # 推断页面
            elif any(kw in title_lower for kw in page_keywords):
                pages.append({
                    'id': topic.id,
                    'name': topic.title,
                    'level': topic.level,
                    'parent': self._find_parent_title(all_topics, topic.parent_id),
                    'features': [child.title for child in topic.children[:10]]
                })

            # 推断功能点
            elif any(kw in title_lower for kw in feature_keywords) or topic.level >= 3:
                features.append({
                    'id': topic.id,
                    'name': topic.title,
                    'level': topic.level,
                    'parent': self._find_parent_title(all_topics, topic.parent_id),
                    'notes': topic.attributes.get('notes', '')
                })

        return modules, pages, features

    def _find_parent_title(self, all_topics: List[XMindNode], parent_id: str) -> str:
        """查找父节点标题"""
        if not parent_id:
            return "根节点"
        for topic in all_topics:
            if topic.id == parent_id:
                return topic.title
        return "未知"

    def _determine_structure(self, root_topic: XMindNode) -> str:
        """确定思维导图结构类型"""
        if not root_topic:
            return "unknown"

        # 基于节点数量和层级判断
        total_children = len(self._flatten_topics(root_topic))
        max_depth = 0
        for node in self._flatten_topics(root_topic):
            max_depth = max(max_depth, node.level)

        if max_depth <= 2:
            return "simple"  # 简单结构
        elif max_depth >= 5:
            return "complex"  # 复杂结构
        elif total_children > 50:
            return "comprehensive"  # 综合系统
        else:
            return "standard"  # 标准结构

    def to_json(self) -> str:
        """转换为JSON"""
        result = self.analyze()
        if result:
            # 转换为可序列化的格式
            data = {
                'file_path': result.file_path,
                'title': result.title,
                'structure_type': result.structure_type,
                'statistics': result.statistics,
                'modules': result.modules,
                'pages': result.pages,
                'features': result.features,
                'all_topics': [
                    {
                        'id': t.id,
                        'title': t.title,
                        'level': t.level,
                        'parent_id': t.parent_id,
                        'children_count': len(t.children),
                        'attributes': t.attributes
                    }
                    for t in result.all_topics
                ]
            }
            return json.dumps(data, ensure_ascii=False, indent=2)
        return "{}"

    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        result = self.analyze()
        if not result:
            return "# XMind分析失败\n无法加载或解析XMind文件。"

        md_lines = []

        md_lines.append("# XMind原型分析报告")
        md_lines.append("")
        md_lines.append(f"**文件路径**: {result.file_path}")
        md_lines.append(f"**主标题**: {result.title}")
        md_lines.append(f"**结构类型**: {result.structure_type}")
        md_lines.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append("")

        md_lines.append("## 统计信息")
        md_lines.append("")
        md_lines.append(f"- **节点总数**: {result.statistics['total_topics']}")
        md_lines.append(f"- **最大层级**: {result.statistics['max_depth']}")
        md_lines.append("")
        md_lines.append("**各层级节点数**:")
        md_lines.append("")
        for level, count in sorted(result.statistics['topics_by_level'].items()):
            md_lines.append(f"- Level {level}: {count} 个节点")
        md_lines.append("")

        # 思维导图结构
        md_lines.append("## 思维导图结构")
        md_lines.append("")
        md_lines.append("```yaml")
        md_lines.append(self._generate_yaml_structure(result.root_topic))
        md_lines.append("```")
        md_lines.append("")

        # 推断的功能模块
        if result.modules:
            md_lines.append("## 功能模块")
            md_lines.append("")
            md_lines.append("| 模块名称 | 层级 | 子节点数 | 包含内容 |")
            md_lines.append("|----------|------|----------|----------|")
            for module in result.modules:
                children_str = ', '.join(module['children'][:5])
                if len(module['children']) > 5:
                    children_str += '...'
                md_lines.append(f"| {module['name']} | L{module['level']} | {module['children_count']} | {children_str} |")
            md_lines.append("")

        # 推断的页面结构
        if result.pages:
            md_lines.append("## 页面结构")
            md_lines.append("")
            md_lines.append("| 页面名称 | 层级 | 所属模块 | 包含功能 |")
            md_lines.append("|----------|------|----------|----------|")
            for page in result.pages:
                features_str = ', '.join(page['features'][:5])
                if len(page['features']) > 5:
                    features_str += '...'
                md_lines.append(f"| {page['name']} | L{page['level']} | {page['parent']} | {features_str} |")
            md_lines.append("")

        # 推断的功能点
        if result.features:
            md_lines.append("## 功能点清单")
            md_lines.append("")
            md_lines.append("| 功能名称 | 层级 | 所属页面 | 备注 |")
            md_lines.append("|----------|------|----------|------|")
            for feature in result.features[:20]:  # 最多显示20个
                md_lines.append(f"| {feature['name']} | L{feature['level']} | {feature['parent']} | {feature['notes'] or '-'} |")
            md_lines.append("")

        # 技术实现建议
        md_lines.append("## 技术实现建议")
        md_lines.append("")

        md_lines.append("### 前端页面路由规划")
        md_lines.append("```typescript")
        md_lines.append("// 基于XMind分析的路由规划")
        md_lines.append("const routes = [")
        md_lines.append("  { path: '/', element: <Layout /> },")
        for page in result.pages[:10]:
            route_path = page['name'].lower().replace(' ', '-').replace('/', '-')
            md_lines.append(f"  {{ path: '/{route_path}', element: <{self._to_component_name(page['name'])} /> }},")
        md_lines.append("];")
        md_lines.append("```")
        md_lines.append("")

        md_lines.append("### 后端API接口规划")
        md_lines.append("```yaml")
        md_lines.append("# 建议的API接口")
        for module in result.modules[:5]:
            api_prefix = module['name'].lower().replace(' ', '-').replace('/', '-')
            md_lines.append(f"api/v1/{api_prefix}:")
            md_lines.append(f"  GET: 获取{module['name']}列表")
            md_lines.append(f"  POST: 创建{module['name']}")
            md_lines.append(f"  PUT: 更新{module['name']}")
            md_lines.append(f"  DELETE: 删除{module['name']}")
        md_lines.append("```")
        md_lines.append("")

        md_lines.append("### 数据库表设计建议")
        md_lines.append("```sql")
        for module in result.modules[:5]:
            table_name = module['name'].lower().replace(' ', '_').replace('/', '_')
            md_lines.append(f"-- {module['name']}表")
            md_lines.append(f"CREATE TABLE {table_name} (")
            md_lines.append(f"    id VARCHAR(36) PRIMARY KEY,")
            md_lines.append(f"    name VARCHAR(100) NOT NULL,")
            md_lines.append(f"    status VARCHAR(20) DEFAULT 'active',")
            md_lines.append(f"    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,")
            md_lines.append(f"    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            md_lines.append(f");")
            md_lines.append("")
        md_lines.append("```")
        md_lines.append("")

        md_lines.append("---")
        md_lines.append("*生成工具: bie-zheng-luan-prototype技能*")
        md_lines.append("*注意: 本分析基于XMind节点结构，具体业务逻辑需要与产品经理确认*")

        return "\n".join(md_lines)

    def _generate_yaml_structure(self, node: XMindNode, indent: int = 0) -> str:
        """生成YAML格式的结构"""
        lines = []
        prefix = "  " * indent

        lines.append(f"{prefix}- {node.title}:")
        lines.append(f"{prefix}  id: {node.id}")
        lines.append(f"{prefix}  level: {node.level}")

        if node.attributes:
            for key, value in node.attributes.items():
                if value:
                    lines.append(f"{prefix}  {key}: {value}")

        if node.children:
            lines.append(f"{prefix}  children:")
            for child in node.children:
                lines.append(self._generate_yaml_structure(child, indent + 2))

        return "\n".join(lines)

    def _to_component_name(self, name: str) -> str:
        """转换为组件名称"""
        # 移除特殊字符，转换为PascalCase
        words = name.replace('/', ' ').replace('-', ' ').split()
        return ''.join(word.capitalize() for word in words)


def main():
    if len(sys.argv) < 2:
        print("用法: python xmind-analyzer.py <XMind文件> [输出格式: markdown|json]")
        print("示例: python xmind-analyzer.py product.xmind markdown")
        print("")
        print("XMind文件格式: .xmind (zip压缩包)")
        sys.exit(1)

    xmind_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "markdown"

    if not Path(xmind_file).exists():
        print(f"错误: XMind文件不存在: {xmind_file}")
        sys.exit(1)

    # 创建分析器
    analyzer = XMindAnalyzer(xmind_file)

    # 输出结果
    if output_format.lower() == "json":
        result = analyzer.to_json()
    else:
        result = analyzer.to_markdown()

    print(result)


if __name__ == "__main__":
    main()