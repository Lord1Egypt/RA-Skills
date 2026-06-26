#!/usr/bin/env python3
"""
电商评论数据处理工具 - 简化版
固定列名匹配，找不到就报错
支持 Excel 文件自动转换
"""

import csv
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class ReviewProcessor:
    """评论数据处理器"""

    # 22维度标签列名
    TAG_COLUMNS = [
        '人群_性别', '人群_年龄段', '人群_职业', '人群_购买角色',
        '场景_使用场景',
        '功能_满意度', '功能_具体功能',
        '质量_材质', '质量_做工', '质量_耐用性',
        '服务_发货速度', '服务_包装质量', '服务_客服响应', '服务_退换货', '服务_保修',
        '体验_舒适度', '体验_易用性', '体验_外观设计', '体验_价格感知',
        '竞品_竞品对比', '复购_复购意愿',
        '情感_总体评价'
    ]

    # 固定列名匹配规则（中英文）
    COLUMN_NAMES = {
        'rating': ['星级', '评分', '打分', 'rating', 'star', 'score', 'stars', 'star-rating', 'src'],
        'title': ['标题', '题目', 'subject', 'title', 'headline'],
        'content': ['内容', '评论', '评价', '反馈', 'content', 'body', 'review', 'comment', 'text', 'message']
    }

    @staticmethod
    def _is_excel_file(file_path: Path) -> bool:
        """判断文件是否为 Excel 格式"""
        excel_extensions = ['.xlsx', '.xls', '.xlsm']
        return file_path.suffix.lower() in excel_extensions

    @staticmethod
    def _convert_excel_to_csv(excel_path: Path) -> Path:
        """将 Excel 文件转换为 CSV（使用 openpyxl）"""
        try:
            import openpyxl
        except ImportError:
            print("📦 正在安装 openpyxl...")
            os.system("pip install openpyxl -q")
            import openpyxl

        print(f"🔄 检测到 Excel 文件，正在转换为 CSV...")

        # 读取 Excel
        wb = openpyxl.load_workbook(excel_path)
        ws = wb.active

        # 创建临时 CSV 文件
        temp_csv = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8-sig', newline='')
        temp_path = Path(temp_csv.name)

        # 写入 CSV
        writer = csv.writer(temp_csv)
        for row in ws.iter_rows(values_only=True):
            # 处理 None 值
            processed_row = [str(cell) if cell is not None else '' for cell in row]
            writer.writerow(processed_row)

        temp_csv.close()

        print(f"✅ Excel 已转换为临时 CSV: {temp_path.name}")
        return temp_path

    @staticmethod
    def _is_css_column(header: str) -> bool:
        """判断是否为CSS类名格式的列"""
        if not header:
            return False
        header_lower = header.lower()

        # 如果以 src 结尾，可能是图片/资源列，不是CSS列
        if header_lower.endswith(' src') or header_lower == 'src':
            return False

        # 包含 __ 和其他 CSS 相关关键词则是CSS列
        has_double_underscore = '__' in header_lower
        css_keywords = ['typography', 'style', 'class', 'css', 'avatar']
        has_css_keywords = any(kw in header_lower for kw in css_keywords)

        return has_double_underscore and has_css_keywords

    def __init__(self, input_csv: str, output_dir: Optional[str] = None):
        """初始化处理器"""
        self.input_path = Path(input_csv)
        if not self.input_path.exists():
            raise FileNotFoundError(f"❌ 文件不存在: {input_csv}")

        # 自动检测并转换 Excel 文件
        self.temp_csv_file = None
        if self._is_excel_file(self.input_path):
            self.temp_csv_file = self._convert_excel_to_csv(self.input_path)
            self.input_csv = self.temp_csv_file
            self.is_excel_converted = True
            print(f"📋 原始文件: {self.input_path.name}")
        else:
            self.input_csv = self.input_path
            self.is_excel_converted = False

        # 从文件名推断产品名
        product_name = self.input_path.stem
        date_str = datetime.now().strftime('%Y%m%d')

        self.output_dir = Path(output_dir or f"output/{product_name}_{date_str}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 检测列索引
        self.column_map = self._detect_columns()

    def _detect_columns(self) -> Dict[str, int]:
        """检测CSV列索引"""
        # 尝试多种编码
        encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'latin1']
        headers = None
        used_encoding = None

        for encoding in encodings:
            try:
                with open(self.input_csv, 'r', encoding=encoding) as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                used_encoding = encoding
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        if headers is None:
            raise ValueError("❌ 无法读取CSV文件，请检查文件编码（支持UTF-8/GBK/GB2312）")

        print(f"   📝 使用编码: {used_encoding}")

        # 转小写用于匹配
        headers_lower = [h.lower() if h else '' for h in headers]

        column_map = {}
        print(f"\n📋 CSV表头检测:")

        for col_type, names in self.COLUMN_NAMES.items():
            found = False
            for idx, header_lower in enumerate(headers_lower):
                # 跳过 CSS 类名列
                if self._is_css_column(headers[idx]):
                    continue

                for name in names:
                    # 使用包含匹配（而不是精确匹配）
                    if name.lower() in header_lower:
                        column_map[col_type] = idx
                        print(f"   ✅ {col_type}: 列{idx} ({headers[idx]})")
                        found = True
                        break
                if found:
                    break

            if not found:
                print(f"   ❌ {col_type}: 未找到")

        # 验证必需列
        required = {'rating', 'content'}
        missing = required - set(column_map.keys())
        if missing:
            print(f"\n❌ 错误: CSV缺少必需列: {missing}")
            print(f"\n📌 你的CSV必须包含以下列名之一:")
            for col_type, names in self.COLUMN_NAMES.items():
                print(f"   {col_type}: {', '.join(names)}")
            print(f"\n💡 请修改你的CSV表头，使其包含上述列名")
            raise ValueError(f"缺少必需列: {missing}")

        return column_map

    def _open_csv(self, mode='r'):
        """打开CSV文件，自动检测编码"""
        encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'latin1']
        last_error = None

        for encoding in encodings:
            try:
                f = open(self.input_csv, mode, encoding=encoding, newline='')
                # 验证是否能正常读取第一行
                if 'r' in mode:
                    first_byte = f.read(1024)
                    f.seek(0)
                return f, encoding
            except (UnicodeDecodeError, UnicodeError) as e:
                last_error = e
                continue

        raise ValueError(f"❌ 无法读取CSV文件，请检查文件编码: {last_error}")

    def read_csv(self, min_length: int = 10) -> List[Dict[str, Any]]:
        """读取CSV文件，提取评论和评分"""
        reviews = []

        f, encoding = self._open_csv()
        try:
            reader = csv.reader(f)
            headers = next(reader)  # 跳过表头

            for row in reader:
                # 跳过空行
                if not row or len(row) <= max(self.column_map.values()):
                    continue

                # 跳过广告行
                if any(ad in str(row).lower() for ad in ['advertisement', 'sponsored', '广告']):
                    continue

                # 解析评分
                rating = self._parse_rating(row[self.column_map['rating']])

                # 提取内容
                content = row[self.column_map['content']] or ""

                # 如果有标题列，合并标题和内容
                if 'title' in self.column_map:
                    title = row[self.column_map['title']] or ""
                    if title and content:
                        content = f"{title}. {content}"
                    elif title:
                        content = title

                content = content.strip()
                # 清理多余空白
                content = ' '.join(content.split())

                if content and len(content) > min_length:
                    reviews.append({
                        "id": len(reviews) + 1,
                        "content": content,
                        "rating": rating
                    })
        finally:
            f.close()

        return reviews

    def _parse_rating(self, value: str) -> int:
        """解析评分"""
        if not value:
            return 3

        value_lower = value.lower()

        # 从SVG URL解析
        if 'stars-5' in value_lower:
            return 5
        elif 'stars-4' in value_lower:
            return 4
        elif 'stars-3' in value_lower:
            return 3
        elif 'stars-2' in value_lower:
            return 2
        elif 'stars-1' in value_lower:
            return 1

        # 从数字解析
        import re
        numbers = re.findall(r'\d+', value)
        if numbers:
            rating = int(numbers[0])
            return max(1, min(5, rating))

        return 3  # 默认

    def create_batches(self, reviews: List[Dict], batch_size: int = 30) -> List[Dict]:
        """将评论分成批次"""
        batches = []
        total_batches = (len(reviews) + batch_size - 1) // batch_size

        for i in range(0, len(reviews), batch_size):
            batch = reviews[i:i+batch_size]
            batches.append({
                "batch_num": len(batches) + 1,
                "total_batches": total_batches,
                "reviews": batch
            })

        return batches

    def save_batch_json(self, reviews: List[Dict], batch_num: int):
        """保存批次为JSON文件"""
        output_file = self.output_dir / f"batch{batch_num}_input.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
        print(f"✅ 批次 {batch_num} 已保存: {output_file}")

    def save_batch_info(self, reviews: List[Dict], batch_size: int = 30):
        """保存批次信息"""
        batches = self.create_batches(reviews, batch_size)

        batch_info = {
            "total_reviews": len(reviews),
            "total_batches": len(batches),
            "batch_size": batch_size,
            "batches": [{"batch_num": b["batch_num"], "count": len(b["reviews"])} for b in batches],
            "column_map": self.column_map
        }

        output_file = self.output_dir / "batch_info.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(batch_info, f, ensure_ascii=False, indent=2)

        return batch_info

    def merge_tags(self, tag_files: List[str] = None) -> List[Dict]:
        """合并多个批次标签文件"""
        if tag_files is None:
            tag_files = sorted(self.output_dir.glob("batch*_tags.json"))
            tag_files = [str(f) for f in tag_files]

        all_tags = []
        for file in tag_files:
            with open(file, 'r', encoding='utf-8') as f:
                tags = json.load(f)
                all_tags.extend(tags)

        print(f"✅ 合并完成: 共 {len(all_tags)} 条标签")
        return all_tags

    def export_csv(self, reviews: List[Dict], tags: List[Dict], filename: str = "reviews_labeled.csv"):
        """导出带标签的CSV文件"""
        tags_dict = {t['review_id']: t for t in tags}

        output_file = self.output_dir / filename
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)

            headers = ['ID', '评分', '评论内容', '情感倾向', '信息密度'] + self.TAG_COLUMNS
            writer.writerow(headers)

            for review in reviews:
                review_id = review['id']
                tag_data = tags_dict.get(review_id, {})

                row = [
                    review_id,
                    review['rating'],
                    review['content'][:500],
                    tag_data.get('sentiment', ''),
                    tag_data.get('info_score', '')
                ]

                tags_obj = tag_data.get('tags', {})
                for col in self.TAG_COLUMNS:
                    row.append(tags_obj.get(col, ''))

                writer.writerow(row)

        print(f"✅ CSV 生成完成: {output_file}")

    def calculate_stats(self, reviews: List[Dict], tags: List[Dict]) -> Dict:
        """计算统计数据"""
        sentiment_counts = {}
        for t in tags:
            s = t['sentiment']
            sentiment_counts[s] = sentiment_counts.get(s, 0) + 1

        rating_dist = {}
        for r in reviews:
            rating = r['rating']
            rating_dist[rating] = rating_dist.get(rating, 0) + 1

        return {
            "total_reviews": len(reviews),
            "total_tagged": len(tags),
            "sentiment_distribution": sentiment_counts,
            "rating_distribution": rating_dist,
            "average_rating": sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0
        }

    def save_stats(self, stats: Dict, filename: str = "stats.json"):
        """保存统计数据"""
        output_file = self.output_dir / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"✅ 统计数据已保存: {output_file}")

    def print_stats(self, stats: Dict):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("📊 统计分析")
        print("=" * 60)
        print(f"总评论数: {stats['total_reviews']}")
        print(f"平均评分: {stats['average_rating']:.2f}/5")

        print("\n情感分布:")
        for s, c in sorted(stats['sentiment_distribution'].items(), key=lambda x: -x[1]):
            pct = c / stats['total_tagged'] * 100
            print(f"  {s}: {c} ({pct:.1f}%)")

        print("\n评分分布:")
        for r, c in sorted(stats['rating_distribution'].items()):
            pct = c / stats['total_reviews'] * 100
            print(f"  {r}星: {c} ({pct:.1f}%)")

    def cleanup(self):
        """清理临时文件（Excel 转换产生的 CSV）"""
        if self.temp_csv_file and self.temp_csv_file.exists():
            try:
                self.temp_csv_file.unlink()
                print(f"🧹 已清理临时文件: {self.temp_csv_file.name}")
            except Exception as e:
                print(f"⚠️  清理临时文件失败: {e}")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='电商评论数据处理工具（支持 CSV 和 Excel 文件）')
    parser.add_argument('input_csv', help='输入文件路径（支持 CSV、XLSX、XLS）')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('-b', '--batch-size', type=int, default=30, help='批次大小 (默认: 30)')
    parser.add_argument('--export-batches', action='store_true', help='导出批次 JSON 文件')
    parser.add_argument('--merge-tags', action='store_true', help='合并标签文件并导出 CSV')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')

    args = parser.parse_args()

    # 初始化处理器（会自动检测并转换 Excel）
    print(f"📂 读取文件: {args.input_csv}")
    processor = ReviewProcessor(args.input_csv, args.output)

    try:
        # 读取数据
        reviews = processor.read_csv()
        print(f"✅ 共读取 {len(reviews)} 条评论")

        # 导出批次
        if args.export_batches:
            batches = processor.create_batches(reviews, args.batch_size)
            for batch in batches:
                processor.save_batch_json(batch['reviews'], batch['batch_num'])
            processor.save_batch_info(reviews, args.batch_size)

        # 合并标签并导出 CSV
        if args.merge_tags:
            tags = processor.merge_tags()
            processor.export_csv(reviews, tags)

            stats = processor.calculate_stats(reviews, tags)
            processor.save_stats(stats)

            if args.stats:
                processor.print_stats(stats)

        # 仅统计
        if args.stats and not args.merge_tags:
            tags = processor.merge_tags()
            stats = processor.calculate_stats(reviews, tags)
            processor.print_stats(stats)

    finally:
        # 清理临时文件（如果有 Excel 转换）
        processor.cleanup()


if __name__ == "__main__":
    main()
