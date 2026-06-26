#!/usr/bin/env python3
"""
Free Keyword Miner - 零成本关键词挖掘工具
支持: Google PAA, Autocomplete, Reddit, Bing
"""
import argparse
import json
import sys
import urllib.request
import urllib.parse
import re
from datetime import datetime

class KeywordMiner:
    def __init__(self, language='en'):
        self.language = language
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.results = {
            'generated_at': datetime.now().isoformat(),
            'google_paa': [],
            'autocomplete': [],
            'reddit_topics': [],
            'bing_related': [],
            'clusters': [],
            'topic_ideas': []
        }
    
    def get_google_paa(self, query, max_results=15):
        """Google People Also Ask"""
        try:
            import people_also_ask as paa
            questions = paa.get_related_questions(query, max_nb_questions=max_results)
            self.results['google_paa'] = list(questions)
            return list(questions)
        except Exception as e:
            print(f"  ⚠️ PAA error: {e}", file=sys.stderr)
            return []
    
    def get_autocomplete(self, query, max_results=20):
        """Google Autocomplete"""
        suggestions = set()
        prefixes = ['', 'best ', 'how to ', 'why ', 'what is ']
        suffixes = ['', ' guide', ' review', ' tips', ' 2026']
        
        for prefix in prefixes:
            for suffix in suffixes:
                q = f"{prefix}{query}{suffix}"
                try:
                    url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl={self.language}&q={urllib.parse.quote(q)}"
                    req = urllib.request.Request(url, headers=self.headers)
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read())
                        if len(data) > 1:
                            for s in data[1]:
                                suggestions.add(s)
                                if len(suggestions) >= max_results:
                                    break
                except:
                    pass
                if len(suggestions) >= max_results:
                    break
        
        self.results['autocomplete'] = list(suggestions)
        return list(suggestions)
    
    def get_reddit_topics(self, query, max_results=10):
        """Reddit讨论挖掘"""
        topics = []
        subreddits = ['sextoys', 'TwoXSex', 'AskWomen', 'sex', 'relationship_advice']
        
        for sub in subreddits:
            try:
                url = f"https://www.reddit.com/r/{sub}/search.json?q={urllib.parse.quote(query)}&restrict_sr=on&limit=5&sort=top&t=year"
                req = urllib.request.Request(url, headers={'User-Agent': 'KeywordMiner/1.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read())
                    for post in data.get('data', {}).get('children', []):
                        d = post['data']
                        if d.get('score', 0) > 5:
                            topics.append({
                                'title': d.get('title', ''),
                                'score': d.get('score', 0),
                                'subreddit': d.get('subreddit', ''),
                                'comments': d.get('num_comments', 0),
                                'pain_points': self._extract_pain_points(d.get('selftext', ''))
                            })
            except:
                pass
        
        topics.sort(key=lambda x: x['score'], reverse=True)
        self.results['reddit_topics'] = topics[:max_results]
        return topics[:max_results]
    
    def get_bing_related(self, query, max_results=10):
        """Bing相关搜索"""
        related = []
        try:
            url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                # 提取相关搜索
                matches = re.findall(r'<a[^>]*class="[^"]*b_algo[^"]*"[^>]*>(.*?)</a>', html)
                for m in matches[:max_results]:
                    clean = re.sub(r'<[^>]+>', '', m).strip()
                    if clean and len(clean) > 5:
                        related.append(clean)
        except Exception as e:
            print(f"  ⚠️ Bing error: {e}", file=sys.stderr)
        
        self.results['bing_related'] = related
        return related
    
    def generate_clusters(self, keywords):
        """关键词聚类"""
        clusters = {}
        for kw in keywords:
            words = kw.lower().split()
            if words:
                key = words[0]
                if key not in clusters:
                    clusters[key] = []
                clusters[key].append(kw)
        
        result = []
        for key, kws in sorted(clusters.items(), key=lambda x: -len(x[1])):
            if len(kws) > 1:
                result.append({'name': f"{key}-cluster", 'keywords': kws[:10]})
        
        self.results['clusters'] = result
        return result
    
    def generate_topics(self, keywords, pain_points):
        """从关键词和痛点生成话题标题"""
        topics = []
        templates = [
            "How to {kw}",
            "Best {kw} 2026",
            "{kw}: Complete Guide",
            "Top 10 {kw}",
            "{kw} Tips and Tricks"
        ]
        
        for kw in keywords[:5]:
            for tmpl in templates[:2]:
                topics.append(tmpl.format(kw=kw))
        
        for pain in pain_points[:5]:
            topics.append(f"How to Solve: {pain[:50]}")
        
        self.results['topic_ideas'] = topics
        return topics
    
    def _extract_pain_points(self, text):
        """从文本提取痛点"""
        pain_keywords = ['problem', 'issue', 'struggle', 'difficult', 'confused', 'frustrated', 'worried', 'embarrassed']
        sentences = text.split('.')
        pains = []
        for s in sentences:
            if any(k in s.lower() for k in pain_keywords):
                pains.append(s.strip()[:100])
        return '; '.join(pains) if pains else ''
    
    def run(self, seed, sources='all', max_results=20):
        """主流程"""
        print(f"🔍 开始挖掘关键词: {seed}")
        print(f"   数据源: {sources}")
        print()
        
        all_keywords = []
        
        if sources in ['all', 'google-paa']:
            print("📰 获取 Google People Also Ask...")
            paa = self.get_google_paa(seed, max_results)
            all_keywords.extend(paa)
            print(f"   ✅ {len(paa)} 个问题")
        
        if sources in ['all', 'autocomplete']:
            print("🔤 获取 Google Autocomplete...")
            auto = self.get_autocomplete(seed, max_results)
            all_keywords.extend(auto)
            print(f"   ✅ {len(auto)} 个建议")
        
        if sources in ['all', 'reddit']:
            print("💬 挖掘 Reddit 讨论...")
            reddit = self.get_reddit_topics(seed, max_results)
            all_keywords.extend([t['title'] for t in reddit])
            print(f"   ✅ {len(reddit)} 个话题")
        
        if sources in ['all', 'bing']:
            print("🔎 获取 Bing 相关搜索...")
            bing = self.get_bing_related(seed, max_results)
            all_keywords.extend(bing)
            print(f"   ✅ {len(bing)} 个相关词")
        
        # 聚类和话题生成
        if all_keywords:
            print("\n📊 生成关键词聚类...")
            self.generate_clusters(all_keywords)
            print(f"   ✅ {len(self.results['clusters'])} 个聚类")
            
            pain_points = [t.get('pain_points', '') for t in self.results['reddit_topics'] if t.get('pain_points')]
            print("💡 生成话题想法...")
            self.generate_topics(all_keywords, pain_points)
            print(f"   ✅ {len(self.results['topic_ideas'])} 个话题")
        
        self.results['total_keywords'] = len(set(all_keywords))
        print(f"\n✅ 完成! 共 {self.results['total_keywords']} 个唯一关键词")
        
        return self.results

def main():
    parser = argparse.ArgumentParser(description='Free Keyword Miner')
    parser.add_argument('--seed', required=True, help='种子关键词')
    parser.add_argument('--sources', default='all', choices=['all', 'google-paa', 'autocomplete', 'reddit', 'bing'])
    parser.add_argument('--output', default='keywords.json', help='输出文件')
    parser.add_argument('--max-results', type=int, default=20, help='每源最大结果数')
    parser.add_argument('--language', default='en', help='语言代码')
    
    args = parser.parse_args()
    
    miner = KeywordMiner(language=args.language)
    results = miner.run(args.seed, args.sources, args.max_results)
    
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 结果已保存: {args.output}")

if __name__ == '__main__':
    main()
