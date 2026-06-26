#!/usr/bin/env python3
"""
Doc Genius - 智能文档处理助手（付费版）
支持PDF/Word/Markdown智能摘要、格式转换、批量处理
集成 SkillPay 计费系统
"""
import sys
import os
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, List, Any
import concurrent.futures
from dataclasses import dataclass, asdict
import requests

# 本地依赖
try:
    import PyPDF2
    from docx import Document
    import markdown
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请安装: pip install PyPDF2 python-docx markdown beautifulsoup4")
    sys.exit(1)

# ═══════════════════════════════════════════════════
# SkillPay Billing Configuration / 计费配置
# ═══════════════════════════════════════════════════
BILLING_API_URL = 'https://skillpay.me'
BILLING_API_KEY = 'sk_0de94ea93e9aca73aafc2b6457b8de378389a21661f9c6ad4e6b7929e390e971'
SKILL_ID = '929eb85f-4a8b-4bb3-bccd-5b7dd80bcd94'  # Doc Genius

VENV_PYTHON = "/Users/gaolei/.openclaw/workspace/.venv/bin/python3"
PRICE_PER_CALL = 0.01  # USDT / 次

# ═══════════════════════════════════════════════════
# Billing Functions / 计费函数
# ═══════════════════════════════════════════════════

def check_balance(user_id: str) -> float:
    """查询用户余额"""
    resp = requests.get(
        f"{BILLING_API_URL}/api/v1/billing/balance",
        params={"user_id": user_id},
        headers={
            'X-API-Key': BILLING_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    data = resp.json()
    return data.get('balance', 0.0)


def charge_user(user_id: str) -> dict:
    """
    扣费（余额不足自动返回充值链接）
    
    Returns:
        {
            "ok": True,  # 扣费成功
            "balance": 10.5
        }
        或
        {
            "ok": False,  # 余额不足
            "balance": 0.02,
            "payment_url": "https://pay.bnbchain.org/..."
        }
    """
    resp = requests.post(
        f"{BILLING_API_URL}/api/v1/billing/charge",
        json={
            "user_id": user_id,
            "skill_id": SKILL_ID,
            "amount": 0  # 0 = 使用 Skill 默认价格
        },
        headers={
            'X-API-Key': BILLING_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    data = resp.json()
    
    if data.get('success'):
        return {
            "ok": True,
            "balance": data.get('balance', 0)
        }
    else:
        return {
            "ok": False,
            "balance": data.get('balance', 0),
            "payment_url": data.get('payment_url', '')
        }


def get_payment_link(user_id: str, amount: float = 8.0) -> str:
    """生成充值链接"""
    resp = requests.post(
        f"{BILLING_API_URL}/api/v1/billing/payment-link",
        json={
            "user_id": user_id,
            "amount": amount
        },
        headers={
            'X-API-Key': BILLING_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    data = resp.json()
    return data.get('payment_url', '')


# ═══════════════════════════════════════════════════
# Document Processing / 文档处理
# ═══════════════════════════════════════════════════

@dataclass
class DocumentInfo:
    """文档信息"""
    file: str
    type: str
    summary: str
    keywords: List[str]
    word_count: int
    pages: Optional[int] = None
    error: Optional[str] = None


class DocumentProcessor:
    """文档处理器（与免费版相同，略）"""
    
    def __init__(self, method: str = "local", model: str = "gpt-3.5-turbo"):
        self.method = method
        self.model = model
        
        # 检查OpenAI API
        try:
            import openai
            self.openai_available = True
        except ImportError:
            self.openai_available = False
        
        if method == "ai" and not self.openai_available:
            print("⚠️ OpenAI未安装，自动切换到本地模式")
            self.method = "local"
        
        if method == "ai" and not os.environ.get("OPENAI_API_KEY"):
            print("⚠️ 未设置OPENAI_API_KEY，自动切换到本地模式")
            self.method = "local"

    def extract_text_pdf(self, file_path: Path) -> tuple:
        """从PDF提取文本"""
        text = []
        pages = 0
        
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages = len(reader.pages)
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
        except Exception as e:
            raise Exception(f"PDF提取失败: {e}")
        
        return '\n'.join(text), pages

    def extract_text_docx(self, file_path: Path) -> str:
        """从Word提取文本"""
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return '\n'.join(paragraphs)
        except Exception as e:
            raise Exception(f"Word提取失败: {e}")

    def extract_text_markdown(self, file_path: Path) -> str:
        """从Markdown提取文本"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            html = markdown.markdown(content)
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text(separator='\n', strip=True)
        except Exception as e:
            raise Exception(f"Markdown提取失败: {e}")

    def extract_text(self, file_path: Path) -> tuple:
        """自动识别格式并提取文本"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            text, pages = self.extract_text_pdf(file_path)
            return text, 'pdf', pages
        elif suffix in ['.docx', '.doc']:
            text = self.extract_text_docx(file_path)
            return text, 'word', None
        elif suffix in ['.md', '.markdown']:
            text = self.extract_text_markdown(file_path)
            return text, 'markdown', None
        elif suffix == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text, 'text', None
        else:
            raise ValueError(f"不支持的格式: {suffix}")

    def summarize_local(self, text: str, max_sentences: int = 5) -> str:
        """本地摘要（TextRank简化版）"""
        sentences = [s.strip() for s in text.split('。') if s.strip()]
        sentences += [s.strip() for s in text.split('.') if s.strip() and s.strip() not in sentences]
        
        if not sentences:
            return "无法生成摘要（文本太短或格式异常）"
        
        word_freq = {}
        for sentence in sentences:
            for word in sentence.split():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sentence_scores = []
        for sentence in sentences:
            score = sum(word_freq.get(word, 0) for word in sentence.split())
            sentence_scores.append((sentence, score))
        
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:max_sentences]]
        
        ordered_summary = []
        for sentence in sentences:
            if sentence in top_sentences:
                ordered_summary.append(sentence)
        
        return '。'.join(ordered_summary[:max_sentences])

    def summarize_ai(self, text: str, max_words: int = 200) -> str:
        """AI摘要（OpenAI API）"""
        if not self.openai_available:
            return self.summarize_local(text)
        
        try:
            import openai
            client = openai.OpenAI()
            
            if len(text) > 10000:
                text = text[:10000] + "..."
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的文档摘要助手。请用简洁、准确的语言总结文档的核心内容。"
                    },
                    {
                        "role": "user",
                        "content": f"请用{max_words}字以内总结以下文档：\n\n{text}"
                    }
                ],
                max_tokens=max_words * 2,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ AI摘要失败，切换到本地模式: {e}")
            return self.summarize_local(text)

    def extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """提取关键词"""
        words = []
        for word in text.split():
            if len(word) > 2 and word not in ['的', '是', '在', '和', '了', 'the', 'a', 'an', 'is', 'are']:
                words.append(word)
        
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words[:max_keywords]]

    def summarize(self, file_path: Path, output_format: str = "json") -> Dict[str, Any]:
        """智能摘要"""
        text, doc_type, pages = self.extract_text(file_path)
        
        if self.method == "ai":
            summary = self.summarize_ai(text)
        else:
            summary = self.summarize_local(text)
        
        keywords = self.extract_keywords(text)
        word_count = len(text.split())
        
        result = DocumentInfo(
            file=str(file_path.name),
            type=doc_type,
            summary=summary,
            keywords=keywords,
            word_count=word_count,
            pages=pages
        )
        
        if output_format == "json":
            return asdict(result)
        else:
            return self._format_as_text(result)

    def _format_as_text(self, doc_info: DocumentInfo) -> str:
        """格式化为文本"""
        text = f"""文件: {doc_info.file}
类型: {doc_info.type}
字数: {doc_info.word_count}
"""
        if doc_info.pages:
            text += f"页数: {doc_info.pages}\n"
        
        text += f"""
摘要:
{doc_info.summary}

关键词: {', '.join(doc_info.keywords)}
"""
        return text


# ═══════════════════════════════════════════════════
# Main / 主函数
# ═══════════════════════════════════════════════════

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='Doc Genius - 智能文档处理助手（付费版）')
    
    parser.add_argument('command', choices=['summarize', 'balance', 'test'], help='命令')
    parser.add_argument('file', type=Path, nargs='?', help='文件路径')
    parser.add_argument('--user-id', required=True, help='用户ID（用于计费）')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    parser.add_argument('--method', choices=['local', 'ai'], default='local', help='摘要方法')
    parser.add_argument('--model', default='gpt-3.5-turbo', help='AI模型')
    parser.add_argument('--skip-charge', action='store_true', help='跳过扣费（测试用）')
    
    args = parser.parse_args()
    
    # ═══════════════════════════════════════════════════
    # 命令：查余额
    # ═══════════════════════════════════════════════════
    if args.command == 'balance':
        balance = check_balance(args.user_id)
        print(f"💰 用户 {args.user_id} 的余额: {balance} USDT")
        return
    
    # ═══════════════════════════════════════════════════
    # 命令：测试
    # ═══════════════════════════════════════════════════
    if args.command == 'test':
        print("🧪 测试扣费流程...")
        
        # 查余额
        balance_before = check_balance(args.user_id)
        print(f"  余额（扣费前）: {balance_before} USDT")
        
        # 扣费
        result = charge_user(args.user_id)
        
        if result['ok']:
            print(f"  ✅ 扣费成功！余额: {result['balance']} USDT")
        else:
            print(f"  ❌ 余额不足！当前余额: {result['balance']} USDT")
            print(f"  充值链接: {result['payment_url']}")
        
        return
    
    # ═══════════════════════════════════════════════════
    # 命令：智能摘要
    # ═══════════════════════════════════════════════════
    if args.command == 'summarize':
        if not args.file:
            print("❌ 错误: 请指定文件路径")
            sys.exit(1)
        
        if not args.file.exists():
            print(f"❌ 错误: 文件不存在 - {args.file}")
            sys.exit(1)
        
        # Step 1: 扣费
        if not args.skip_charge:
            print(f"💳 正在扣费 ${PRICE_PER_CALL} USDT...")
            
            charge_result = charge_user(args.user_id)
            
            if not charge_result['ok']:
                print(f"❌ 余额不足！当前余额: {charge_result['balance']} USDT")
                print(f"💰 充值链接: {charge_result['payment_url']}")
                sys.exit(1)
            
            print(f"✅ 扣费成功！剩余余额: {charge_result['balance']} USDT")
        else:
            print("⚠️ 跳过扣费（测试模式）")
        
        # Step 2: 执行文档处理
        print(f"\n📄 正在处理文档: {args.file.name}")
        
        try:
            processor = DocumentProcessor(method=args.method, model=args.model)
            result = processor.summarize(args.file, args.format)
            
            print("\n" + "="*60)
            
            if args.format == 'json':
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(result)
            
            print("="*60)
            print("\n✅ 处理完成！")
        
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
