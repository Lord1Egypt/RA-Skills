import json
import os
from typing import List, Dict, Optional


class GoogleSkill:
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), 'products.json')
        self.products: List[Dict] = []
        self.categories: List[str] = []
        self._load_data()

    def _load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.products = data.get('products', [])
            self.categories = data.get('categories', [])

    def get_all_products(self) -> List[Dict]:
        return self.products

    def get_products_by_category(self, category: str) -> List[Dict]:
        return [p for p in self.products if p.get('category') == category]

    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        for product in self.products:
            if product.get('id') == product_id:
                return product
        return None

    def search_products(self, keyword: str) -> List[Dict]:
        keyword = keyword.lower()
        results = []
        for product in self.products:
            name = product.get('name', '').lower()
            desc = product.get('description', '').lower()
            if keyword in name or keyword in desc:
                results.append(product)
        return results

    def display_products(self, products: List[Dict] = None):
        if products is None:
            products = self.products

        print("\n" + "=" * 60)
        print("Google 全家桶入口".center(60))
        print("=" * 60)

        current_category = None
        for product in products:
            category = product.get('category', '')
            if category != current_category:
                current_category = category
                print(f"\n📂 {category}")
                print("-" * 60)

            icon = product.get('icon', '')
            name = product.get('name', '')
            desc = product.get('description', '')
            url = product.get('url', '')
            print(f"\n  {icon} {name}")
            print(f"     {desc}")
            print(f"     🔗 {url}")

        print("\n" + "=" * 60)

    def display_categories(self):
        print("\n📂 可用分类:")
        for i, category in enumerate(self.categories, 1):
            print(f"  {i}. {category}")

    def open_product(self, product_id: str):
        product = self.get_product_by_id(product_id)
        if product:
            url = product.get('url')
            print(f"\n🚀 正在打开: {product.get('name')}")
            print(f"   链接: {url}")
            import webbrowser
            webbrowser.open(url)
            return True
        else:
            print(f"\n❌ 未找到 ID 为 '{product_id}' 的产品")
            return False


def main():
    skill = GoogleSkill()

    print("🔍 Google 全家桶入口 Skill")
    print("=" * 60)

    while True:
        print("\n请选择操作:")
        print("  1. 查看所有产品")
        print("  2. 按分类查看")
        print("  3. 搜索产品")
        print("  4. 打开产品")
        print("  5. 退出")

        choice = input("\n请输入选项 (1-5): ").strip()

        if choice == "1":
            skill.display_products()

        elif choice == "2":
            skill.display_categories()
            cat_choice = input("\n请选择分类编号: ").strip()
            try:
                cat_index = int(cat_choice) - 1
                if 0 <= cat_index < len(skill.categories):
                    category = skill.categories[cat_index]
                    products = skill.get_products_by_category(category)
                    skill.display_products(products)
                else:
                    print("❌ 无效的分类编号")
            except ValueError:
                print("❌ 请输入有效的数字")

        elif choice == "3":
            keyword = input("请输入搜索关键词: ").strip()
            if keyword:
                results = skill.search_products(keyword)
                if results:
                    print(f"\n✅ 找到 {len(results)} 个结果:")
                    skill.display_products(results)
                else:
                    print(f"\n❌ 未找到包含 '{keyword}' 的产品")

        elif choice == "4":
            print("\n📋 产品 ID 列表:")
            for product in skill.products:
                print(f"  {product.get('id'):<15} - {product.get('name')}")
            product_id = input("\n请输入产品 ID: ").strip()
            if product_id:
                skill.open_product(product_id)

        elif choice == "5":
            print("\n👋 再见！")
            break

        else:
            print("❌ 无效的选项，请重新输入")


if __name__ == "__main__":
    main()
