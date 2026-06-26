#!/usr/bin/env python3
"""
Geekbench 6 跑分数据爬虫和分析工具
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import time
import os

class GeekbenchCrawler:
    BASE_URL = "https://browser.geekbench.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def search_device(self, device_name: str) -> List[Dict]:
        """搜索设备跑分结果"""
        print(f"🔍 搜索设备: {device_name}")

        search_url = f"{self.BASE_URL}/v6/cpu/search"
        params = {'q': device_name}

        try:
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            results = self._parse_search_results(response.text)
            return results
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []

    def _parse_search_results(self, html: str) -> List[Dict]:
        """解析搜索结果页面"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []

        for link in soup.find_all('a', href=re.compile(r'/v6/cpu/\d+')):
            try:
                href = link.get('href', '')
                benchmark_id = href.split('/')[-1]

                parent = link.find_parent(['div', 'tr', 'li'])
                if parent:
                    text = parent.get_text(strip=True)
                    results.append({
                        'id': benchmark_id,
                        'url': f"{self.BASE_URL}{href}",
                        'text': text
                    })
            except Exception:
                continue

        return results

    def get_benchmark_detail(self, benchmark_id: str) -> Optional[Dict]:
        """获取单个跑分详情"""
        url = f"{self.BASE_URL}/v6/cpu/{benchmark_id}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return self._parse_benchmark_detail(response.text, benchmark_id)
        except Exception as e:
            print(f"❌ 获取跑分详情失败 {benchmark_id}: {e}")
            return None

    def _parse_benchmark_detail(self, html: str, benchmark_id: str) -> Dict:
        """解析跑分详情页面"""
        soup = BeautifulSoup(html, 'html.parser')

        data = {
            'id': benchmark_id,
            'url': f"{self.BASE_URL}/v6/cpu/{benchmark_id}",
            'version': '',
            'model': '',
            'operating_system': '',
            'cpu': {
                'name': '',
                'cores': 0,
                'clusters': [],
                'frequency': '',
                'instruction_sets': ''
            },
            'single_core_score': 0,
            'multi_core_score': 0,
            'single_core_details': {},
            'multi_core_details': {},
            'upload_date': '',
            'platform': ''
        }

        # 解析版本号
        version_elem = soup.find(string=re.compile(r'Geekbench \d+\.\d+\.\d+'))
        if version_elem:
            match = re.search(r'Geekbench (\d+\.\d+\.\d+)', str(version_elem))
            if match:
                data['version'] = match.group(1)

        # 解析总分数
        score_containers = soup.find_all('div', class_='score-container')
        for container in score_containers:
            score_div = container.find('div', class_='score')
            note_div = container.find('div', class_='note')

            if score_div and note_div:
                try:
                    score = int(score_div.get_text(strip=True))
                    note = note_div.get_text(strip=True)

                    if 'Single' in note:
                        data['single_core_score'] = score
                    elif 'Multi' in note:
                        data['multi_core_score'] = score
                except (ValueError, AttributeError):
                    continue

        # 解析系统信息表格 - 表格0: 上传信息, 表格1: 系统信息
        tables = soup.find_all('table')
        if len(tables) > 1:
            # 解析系统信息（表格1）
            sys_table = tables[1]
            for row in sys_table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)

                    if 'Model' in label:
                        data['model'] = value
                    elif 'Operating System' in label:
                        data['operating_system'] = value
                    elif 'Platform' in label:
                        data['platform'] = value

            # 解析CPU信息（表格2）
            if len(tables) > 2:
                cpu_table = tables[2]
                for row in cpu_table.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True)
                        value = cells[1].get_text(strip=True)

                        if 'Name' in label:
                            data['cpu']['name'] = value
                        elif 'Topology' in label:
                            cores_match = re.search(r'(\d+)\s*Cores?', value)
                            if cores_match:
                                data['cpu']['cores'] = int(cores_match.group(1))

        # 解析CPU详细信息（从文本中提取）
        cpu_section = soup.find('div', class_='cpu')
        if cpu_section:
            cpu_text = cpu_section.get_text()

            freq_match = re.search(r'(\d+\.?\d*)\s*GHz', cpu_text)
            if freq_match:
                data['cpu']['frequency'] = freq_match.group(1) + ' GHz'

            clusters = re.findall(r'Cluster\s*(\d+)\s*(\d+)\s*Cores?\s*@\s*([\d.]+)\s*GHz', cpu_text)
            for cluster in clusters:
                data['cpu']['clusters'].append({
                    'cluster': int(cluster[0]),
                    'cores': int(cluster[1]),
                    'frequency': cluster[2] + ' GHz'
                })

        # 解析单项得分
        data['single_core_details'] = self._parse_subscores(soup, 'Single-Core')
        data['multi_core_details'] = self._parse_subscores(soup, 'Multi-Core')

        return data

    def _parse_subscores(self, soup: BeautifulSoup, section: str) -> Dict:
        """解析单项得分"""
        scores = {}

        headers = soup.find_all('h3')
        target_header = None
        for h in headers:
            if h.get_text(strip=True) == f'{section} Performance':
                target_header = h
                break

        if target_header:
            next_sibling = target_header.find_next_sibling()
            while next_sibling:
                if next_sibling.name == 'table':
                    for row in next_sibling.find_all('tr'):
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            name = cells[0].get_text(strip=True)
                            score = cells[1].get_text(strip=True)
                            if name and score:
                                try:
                                    scores[name] = int(score)
                                except ValueError:
                                    continue
                    break
                next_sibling = next_sibling.find_next_sibling()

        return scores

    def get_latest_benchmarks(self, limit: int = 50) -> List[Dict]:
        """获取最新上传的跑分结果"""
        url = f"{self.BASE_URL}/v6/cpu"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return self._parse_latest_list(response.text, limit)
        except Exception as e:
            print(f"❌ 获取最新跑分失败: {e}")
            return []

    def _parse_latest_list(self, html: str, limit: int = 50) -> List[Dict]:
        """解析最新跑分列表"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []

        for link in soup.find_all('a', href=re.compile(r'/v6/cpu/\d+'))[:limit]:
            try:
                href = link.get('href', '')
                benchmark_id = href.split('/')[-1]

                parent = link.find_parent('div')
                if parent:
                    text = parent.get_text(strip=True)

                    # 尝试提取设备名称
                    name = link.get_text(strip=True) or text.split('\n')[0][:50]

                    results.append({
                        'id': benchmark_id,
                        'url': f"{self.BASE_URL}{href}",
                        'title': name,
                        'raw_text': text[:200],
                        'single_core': None,  # 列表页没有分数
                        'multi_core': None
                    })
            except Exception:
                continue

        return results

    def get_benchmark_scores(self, benchmark_id: str) -> Optional[Dict]:
        """快速获取单个跑分的分数（不带详情解析）"""
        url = f"{self.BASE_URL}/v6/cpu/{benchmark_id}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            score_containers = soup.find_all('div', class_='score-container')
            for container in score_containers:
                score_div = container.find('div', class_='score')
                note_div = container.find('div', class_='note')

                if score_div and note_div:
                    try:
                        score = int(score_div.get_text(strip=True))
                        note = note_div.get_text(strip=True)

                        if 'Single' in note:
                            single = score
                        elif 'Multi' in note:
                            multi = score
                    except (ValueError, AttributeError):
                        continue

            return {'single_core': single, 'multi_core': multi}
        except Exception:
            return None

    def analyze_device_benchmarks(self, device_model: str) -> Dict:
        """分析特定设备的所有跑分结果"""
        print(f"\n📊 开始分析设备: {device_model}")

        search_results = self.search_device(device_model)

        if not search_results:
            print(f"❌ 未找到设备: {device_model}")
            return {}

        all_benchmarks = []
        for result in search_results[:20]:
            detail = self.get_benchmark_detail(result['id'])
            if detail:
                all_benchmarks.append(detail)
                time.sleep(0.5)

        if not all_benchmarks:
            print("❌ 无法获取跑分详情")
            return {}

        version_stats = {}
        for bench in all_benchmarks:
            version = bench.get('version', 'Unknown')
            if version not in version_stats:
                version_stats[version] = {
                    'count': 0,
                    'single_core_scores': [],
                    'multi_core_scores': [],
                    'benchmarks': []
                }

            version_stats[version]['count'] += 1
            version_stats[version]['single_core_scores'].append(bench['single_core_score'])
            version_stats[version]['multi_core_scores'].append(bench['multi_core_score'])
            version_stats[version]['benchmarks'].append(bench)

        for version, stats in version_stats.items():
            stats['avg_single'] = sum(stats['single_core_scores']) / len(stats['single_core_scores'])
            stats['avg_multi'] = sum(stats['multi_core_scores']) / len(stats['multi_core_scores'])
            stats['median_single'] = self._calculate_median(stats['single_core_scores'])
            stats['median_multi'] = self._calculate_median(stats['multi_core_scores'])

            sorted_single = sorted(enumerate(stats['single_core_scores']),
                                  key=lambda x: abs(x[1] - stats['median_single']))
            sorted_multi = sorted(enumerate(stats['multi_core_scores']),
                                  key=lambda x: abs(x[1] - stats['median_multi']))

            if sorted_single:
                idx = sorted_single[0][0]
                stats['typical_single_core'] = stats['benchmarks'][idx]
            if sorted_multi:
                idx = sorted_multi[0][0]
                stats['typical_multi_core'] = stats['benchmarks'][idx]

        return {
            'device': device_model,
            'total_benchmarks': len(all_benchmarks),
            'versions': version_stats
        }

    def _calculate_median(self, values: List[int]) -> float:
        """计算中位数"""
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        if n % 2 == 0:
            return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
        return sorted_vals[n//2]

    def save_results(self, results: Dict, filename: str = None):
        """保存结果到JSON文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"geekbench_results_{timestamp}.json"

        filepath = os.path.join('/Users/ding/.openclaw/workspace/geekbench', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"💾 结果已保存到: {filepath}")
        return filepath

    def generate_report(self, analysis: Dict) -> str:
        """生成分析报告"""
        if not analysis:
            return "❌ 无数据可生成报告"

        report_lines = [
            f"📱 设备: {analysis['device']}",
            f"📈 总跑分数: {analysis['total_benchmarks']}",
            "-" * 60
        ]

        for version, stats in analysis['versions'].items():
            report_lines.extend([
                f"\n🔹 Geekbench {version}",
                f"  跑分数量: {stats['count']}",
                f"  Single-Core 平均分: {stats['avg_single']:.0f} (中位数: {stats['median_single']:.0f})",
                f"  Multi-Core 平均分: {stats['avg_multi']:.0f} (中位数: {stats['median_multi']:.0f})"
            ])

            if 'typical_single_core' in stats:
                typical = stats['typical_single_core']
                report_lines.append(
                    f"  📌 典型 Single-Core 跑分: "
                    f"[#{typical['id']}]({typical['url']}) "
                    f"(Single: {typical['single_core_score']}, Multi: {typical['multi_core_score']})"
                )

            if 'typical_multi_core' in stats:
                typical = stats['typical_multi_core']
                report_lines.append(
                    f"  📌 典型 Multi-Core 跑分: "
                    f"[#{typical['id']}]({typical['url']}) "
                    f"(Single: {typical['single_core_score']}, Multi: {typical['multi_core_score']})"
                )

        report_lines.append("-" * 60)

        return '\n'.join(report_lines)


def main():
    """主函数示例"""
    crawler = GeekbenchCrawler()

    print("📋 获取最新跑分结果...")
    latest = crawler.get_latest_benchmarks(10)
    for item in latest[:5]:
        print(f"  #{item['id']}: {item['title']} - Single: {item['single_core']}, Multi: {item['multi_core']}")

    print("\n📊 测试获取跑分详情...")
    detail = crawler.get_benchmark_detail('16471550')
    if detail:
        print(f"  型号: {detail['model']}")
        print(f"  操作系统: {detail['operating_system']}")
        print(f"  CPU: {detail['cpu']['name']}")
        print(f"  分数: Single={detail['single_core_score']}, Multi={detail['multi_core_score']}")


if __name__ == '__main__':
    main()
