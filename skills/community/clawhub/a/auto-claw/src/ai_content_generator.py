"""
AI Content Generator — WordPress AI内容生成写入源码
支持多内容类型 / 自动发布 / Gate Pipeline审批
"""
import re
import json
import time
import hashlib
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class ContentSpec:
    """内容规格"""
    spec_id: str
    content_type: str = "blog_post"  # blog_post / product_description / landing_copy / email_sequence
    title: str = ""
    target_keyword: str = ""
    tone: str = "professional"  # professional / casual / urgent / friendly
    length: str = "medium"  # short(300) / medium(600) / long(1200) / comprehensive(2000)
    cta: str = ""  # call to action
    
    # SEO
    primary_keyword: str = ""
    secondary_keywords: List[str] = field(default_factory=list)
    meta_description: str = ""
    
    # 来源
    source_reference: str = ""  # 参考文档/URL
    
    @property
    def word_count_target(self) -> int:
        lengths = {"short": 300, "medium": 600, "long": 1200, "comprehensive": 2000}
        return lengths.get(self.length, 600)

@dataclass
class GeneratedContent:
    """生成的内容"""
    content_id: str
    spec: ContentSpec
    
    title: str = ""
    body: str = ""
    excerpt: str = ""
    meta_description: str = ""
    
    # SEO
    slug: str = ""
    h2_headings: List[str] = field(default_factory=list)
    internal_links: List[str] = field(default_factory=list)
    
    # 质量
    quality_score: float = 0.0  # 0-100
    readability_score: float = 0.0
    
    # 状态
    status: str = "draft"  # draft / pending_review / approved / published
    generated_at: str = ""
    reviewed_by: str = ""
    published_at: str = ""

class AIContentGenerator:
    """
    WordPress AI内容生成引擎
    
    功能：
    1. 多类型内容生成（博客/产品描述/落地页/邮件序列）
    2. SEO优化内容（关键词/H2/内部链接）
    3. 自动生成Meta/Slug/Excerpt
    4. 可读性评分
    5. GATE Pipeline审批流程
    6. 直接写入WordPress源码
    """
    
    # 提示词模板
    PROMPT_TEMPLATES = {
        "blog_post": '''生成一篇SEO优化的博客文章。

要求：
- 标题：{title}
- 主关键词：{keyword}
- 次关键词：{secondary}
- 语气：{tone}
- 字数：约{word_count}字
- CTA：{cta}

格式要求：
- 使用多个H2子标题
- 包含开篇钩子
- 包含结论和CTA
- 包含1-2个FAQ（用H2格式）

输出JSON格式：
{{"title": "...", "body": "...(Markdown)", "excerpt": "...(50字以内)", "meta_description": "...(160字以内)", "h2s": ["...", "..."]}}''',
        
        "product_description": '''生成产品描述。

要求：
- 产品名：{title}
- 目标关键词：{keyword}
- 语气：{tone}
- 字数：约{word_count}字

格式要求：
- 3个要点（Bullet points）
- 包含痛点→解决方案框架
- 包含社会证明占位符
- 包含CTA

输出JSON格式：
{{"title": "...", "body": "...(Markdown)", "excerpt": "..." }}''',
        
        "landing_copy": '''生成高转化落地页文案。

要求：
- 核心信息：{title}
- 目标关键词：{keyword}
- 语气：{tone}
- 字数：约{word_count}字

结构：
1. Hero区：大标题 + 副标题 + CTA
2. 问题区：描述目标受众的痛苦
3. 解决方案区：产品/服务介绍
4. 信任区：社会证明
5. CTA区：最终号召

输出JSON格式：
{{"hero_headline": "...", "hero_sub": "...", "body": "...", "cta": "...", "meta_description": "..."}}'''
    }
    
    def __init__(self, web_root: str = "", llm_api_url: str = "", llm_api_key: str = ""):
        self.web_root = web_root
        self.llm_api_url = llm_api_url
        self.llm_api_key = llm_api_key
        self.contents: Dict[str, GeneratedContent] = {}
        self.pending_review: List[str] = []
    
    def create_spec(self, content_type: str, title: str,
                   keyword: str = "", tone: str = "professional",
                   length: str = "medium", cta: str = "",
                   secondary: List[str] = None) -> ContentSpec:
        """创建内容规格"""
        spec_id = hashlib.md5(f"{title}{time.time()}".encode()).hexdigest()[:8]
        spec = ContentSpec(
            spec_id=spec_id,
            content_type=content_type,
            title=title,
            target_keyword=keyword,
            primary_keyword=keyword,
            secondary_keywords=secondary or [],
            tone=tone,
            length=length,
            cta=cta
        )
        return spec
    
    def generate_content(self, spec: ContentSpec) -> GeneratedContent:
        """生成内容（使用LLM或回退到模板）"""
        content_id = hashlib.md5(f"{spec.title}{time.time()}".encode()).hexdigest()[:8]
        
        # 构建提示词
        template = self.PROMPT_TEMPLATES.get(spec.content_type, self.PROMPT_TEMPLATES["blog_post"])
        prompt = template.format(
            title=spec.title,
            keyword=spec.primary_keyword,
            secondary=", ".join(spec.secondary_keywords),
            tone=spec.tone,
            word_count=spec.word_count_target,
            cta=spec.cta
        )
        
        generated = GeneratedContent(
            content_id=content_id,
            spec=spec,
            title=spec.title,
            generated_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # 尝试LLM调用
        if self.llm_api_url and self.llm_api_key:
            try:
                result = self._call_llm(prompt)
                if result:
                    generated = self._parse_llm_result(result, spec, content_id)
            except Exception as e:
                generated.body = self._generate_fallback_content(spec)
        else:
            # 使用回退模板生成
            generated = self._generate_with_fallback(spec, content_id)
        
        # 计算质量分
        generated = self._score_content(generated)
        
        self.contents[content_id] = generated
        return generated
    
    def _call_llm(self, prompt: str) -> Optional[str]:
        """调用LLM API"""
        import urllib.request
        
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }).encode()
        
        req = urllib.request.Request(
            self.llm_api_url + "/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.llm_api_key}",
                "Content-Type": "application/json"
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    
    def _generate_fallback_content(self, spec: ContentSpec) -> str:
        """使用回退模板生成内容"""
        keyword = spec.primary_keyword
        title = spec.title
        
        if spec.content_type == "blog_post":
            return f'''# {title}

## 开篇

在当今竞争激烈的市场中，{keyword}已经成为企业增长的关键驱动力。本文将深入探讨如何通过优化{keyword}来实现业务突破。

## 什么是{keyword}？

{keyword}不仅仅是一个流行词——它代表了一种全新的商业思维。通过正确的方法和工具，企业可以实现显著的效率提升和成本节约。

## 为什么{keyword}很重要？

1. **效率提升**：自动化流程，减少人工错误
2. **成本优化**：智能资源配置，降低运营成本
3. **可扩展性**：随着业务增长，系统无缝扩展

## 如何开始？

开始使用{keyword}比你想象的要简单。以下是推荐的下一步：

- 评估你当前的流程和痛点
- 研究行业最佳实践
- 选择适合你业务需求的解决方案
- 从小规模试点开始，逐步扩大

## 常见问题

### {keyword}需要多长时间见效？

大多数企业在实施后30-60天内开始看到明显效果。

### 需要多大的团队来管理{keyword}？

实际上，{keyword}的目的是减少人工工作量。一个小型团队甚至个人就可以管理整个系统。

## 结论

{keyword}是现代企业不可或缺的竞争优势。立即开始你的{keyword}之旅吧。

**{spec.cta or "联系我们了解更多"}**
'''
        elif spec.content_type == "product_description":
            return f'''## {title}

**解决你的痛点，提高效率，降低成本。**

### 核心优势

- 🚀 **快速部署**：即开即用，30分钟完成设置
- 💰 **成本节约**：平均降低40%运营成本
- 🔒 **企业级安全**：SOC 2认证，99.99%可用性
- 📊 **可衡量ROI**：清晰的KPI追踪和报告

### 客户证言

> "使用{title}后，我们的团队效率提升了3倍。" — [客户名称]

### 立即开始

{title}提供14天免费试用。{spec.cta or "立即注册"} →

**特点**：{keyword} | 高效 | 可靠
'''
        
        return f"## {title}\n\n内容生成中...\n\n关键词: {keyword}"
    
    def _generate_with_fallback(self, spec: ContentSpec, content_id: str) -> GeneratedContent:
        """使用回退内容生成"""
        body = self._generate_fallback_content(spec)
        
        # 提取H2
        h2s = re.findall(r'^## (.+)$', body, re.MULTILINE)
        
        # 生成摘要
        excerpt = re.sub(r'[#*🚀💰🔒📊>]', '', body[:200]).strip()[:120] + "..."
        
        # 生成slug
        slug = re.sub(r'[^a-z0-9]+', '-', spec.title.lower()).strip('-')[:50]
        
        return GeneratedContent(
            content_id=content_id,
            spec=spec,
            title=spec.title,
            body=body,
            excerpt=excerpt,
            meta_description=spec.meta_description or f"了解关于{spec.primary_keyword}的完整指南。{spec.cta or '立即开始'}",
            slug=slug,
            h2_headings=h2s,
            generated_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _parse_llm_result(self, result: str, spec: ContentSpec, content_id: str) -> GeneratedContent:
        """解析LLM返回"""
        try:
            data = json.loads(result)
        except:
            # 尝试提取JSON
            match = re.search(r'\{[\s\S]+\}', result)
            if match:
                data = json.loads(match.group())
            else:
                return self._generate_with_fallback(spec, content_id)
        
        h2s = data.get("h2s", data.get("sections", []))
        slug = re.sub(r'[^a-z0-9]+', '-', data.get("title", spec.title).lower()).strip('-')[:50]
        
        return GeneratedContent(
            content_id=content_id,
            spec=spec,
            title=data.get("title", spec.title),
            body=data.get("body", ""),
            excerpt=data.get("excerpt", "")[:120],
            meta_description=data.get("meta_description", "")[:160],
            slug=slug,
            h2_headings=h2s if isinstance(h2s, list) else [],
            generated_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _score_content(self, content: GeneratedContent) -> GeneratedContent:
        """内容质量评分"""
        body = content.body
        
        # 可读性（简化版：句子长度）
        sentences = re.split(r'[.!?。]', body)
        avg_sentence_len = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
        if avg_sentence_len < 15:
            readability = 90
        elif avg_sentence_len < 25:
            readability = 75
        else:
            readability = 55
        
        content.readability_score = readability
        
        # 质量分（基于多个因素）
        score = 50
        
        # 有H2
        if content.h2_headings:
            score += 10
        
        # 有CTA
        if content.spec.cta or "CTA" in content.body.upper():
            score += 10
        
        # 有内部链接占位符
        if content.body.count("http") >= 1:
            score += 10
        
        # 可读性
        score += int(readability / 10)
        
        # 长度达标
        word_count = len(body.split())
        target = content.spec.word_count_target
        if target * 0.8 <= word_count <= target * 1.2:
            score += 10
        
        content.quality_score = min(100, score)
        
        return content
    
    def submit_for_review(self, content_id: str) -> bool:
        """提交审批"""
        content = self.contents.get(content_id)
        if not content:
            return False
        
        content.status = "pending_review"
        self.pending_review.append(content_id)
        return True
    
    def approve_content(self, content_id: str, reviewer: str = "auto") -> bool:
        """审批通过"""
        content = self.contents.get(content_id)
        if not content:
            return False
        
        content.status = "approved"
        content.reviewed_by = reviewer
        if content_id in self.pending_review:
            self.pending_review.remove(content_id)
        return True
    
    def get_wp_post_commands(self, content: GeneratedContent, author_id: int = 1) -> List[str]:
        """生成WP-CLI命令"""
        cmds = []
        
        # 创建文章
        body_escaped = content.body.replace('"', '\\"').replace("'", "\\'")
        title_escaped = content.title.replace('"', '\\"')
        excerpt_escaped = content.excerpt.replace('"', '\\"')[:120]
        
        cmd = f'/usr/local/bin/wp post create --post_type=post --post_title="{title_escaped}" --post_content="{body_escaped}" --post_excerpt="{excerpt_escaped}" --post_status=draft --post_author={author_id}'
        cmds.append({"action": "create_post", "cmd": cmd})
        
        # 设置SEO meta
        if content.meta_description:
            meta_escaped = content.meta_description.replace('"', '\\"')
            cmds.append({"action": "set_meta", "cmd": f'/usr/local/bin/wp post meta update __POST_ID__ _yoast_wpseo_metadesc "{meta_escaped}"'})
        
        # 设置slug
        if content.slug:
            cmds.append({"action": "set_slug", "cmd": f"/usr/local/bin/wp post update __POST_ID__ --post_name={content.slug}"})
        
        return cmds
    
    def export_as_wp_import(self, content: GeneratedContent) -> str:
        """导出为WXR格式"""
        return f'''<!-- WXR Fragment for: {content.title} -->
<!-- Title: {content.title} -->
<!-- Status: draft -->
<!-- Generated: {content.generated_at} -->
<!-- Quality Score: {content.quality_score}/100 -->
<!-- Readability: {content.readability_score}/100 -->

{content.body}

<!-- Excerpt: {content.excerpt} -->
<!-- Meta: {content.meta_description} -->'''

def demo():
    gen = AIContentGenerator(
        web_root="/www/wwwroot/linghangyuan1234.dpdns.org"
    )
    
    # 创建规格
    spec = gen.create_spec(
        content_type="blog_post",
        title="如何通过AI驱动SEO在2026年获得10倍流量增长",
        keyword="AI SEO",
        tone="professional",
        length="long",
        cta="获取免费SEO诊断"
    )
    
    # 生成内容
    print("\n🤖 正在生成内容...")
    content = gen.generate_content(spec)
    
    print(f"\n📝 生成完成: {content.title}")
    print(f"   质量分: {content.quality_score}/100")
    print(f"   可读性: {content.readability_score}/100")
    print(f"   字数: {len(content.body.split())}字")
    print(f"   H2章节: {len(content.h2_headings)}个")
    print(f"   状态: {content.status}")
    
    # 提交审批
    gen.submit_for_review(content.content_id)
    print(f"\n✅ 已提交审批")
    
    # 审批通过
    gen.approve_content(content.content_id, "CTO")
    print(f"✅ 已审批通过")
    
    # WP命令
    cmds = gen.get_wp_post_commands(content)
    print(f"\n📋 WP-CLI命令:")
    for c in cmds[:2]:
        print(f"   {c['action']}: {c['cmd'][:70]}...")
    
    # 导出
    wxr = gen.export_as_wp_import(content)
    print(f"\n📦 WXR导出: {len(wxr)}字符")

if __name__ == "__main__":
    demo()
