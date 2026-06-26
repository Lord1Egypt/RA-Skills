"""
Amazon竞品搜索与分析模块
功能：根据品类关键词搜索竞品，进行对比分析
"""
import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright


def search_competitors(keyword, max_results=10, zip_code="10001"):
    """
    搜索竞品
    返回竞品列表（ASIN、标题、价格、评分、评论数）
    """
    async def _search():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                locale='en-US',
                extra_http_headers={
                    'Accept-Language': 'en-US,en;q=0.9'
                }
            )
            page = await context.new_page()
            
            # 搜索URL
            search_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}&s=review-rank"
            print(f"搜索URL: {search_url}")
            
            await page.goto(search_url, wait_until='domcontentloaded', timeout=120000)
            await asyncio.sleep(5)
            
            # 设置邮编以获取美元价格
            try:
                location_btn = await page.query_selector('#glow-ingress-line2')
                if location_btn:
                    await location_btn.click()
                    await asyncio.sleep(3)
                
                zip_input = await page.query_selector('#GLUXZipUpdateInput')
                if zip_input:
                    await zip_input.fill(zip_code)
                    await asyncio.sleep(1)
                    
                    submit_btn = await page.query_selector('#GLUXZipUpdate')
                    if submit_btn:
                        await submit_btn.click()
                        await asyncio.sleep(8)
                        # 刷新页面使价格更新
                        await page.reload(wait_until='domcontentloaded')
                        await asyncio.sleep(3)
            except Exception as e:
                print(f"设置邮编时出错: {e}")
            
            # 查找搜索结果
            products = []
            
            # 尝试多种选择器来获取搜索结果
            search_results = await page.query_selector_all('[data-component-type="s-search-result"]')
            
            if not search_results:
                # 备选选择器
                search_results = await page.query_selector_all('.s-result-item')
            
            print(f"找到 {len(search_results)} 个搜索结果")
            
            for i, item in enumerate(search_results[:max_results]):
                try:
                    # 获取ASIN
                    asin = await item.get_attribute('data-asin')
                    if not asin:
                        continue
                    
                    # 获取标题
                    title_el = await item.query_selector('h2 .a-link-normal span, .a-size-medium.a-color-base.a-text-normal')
                    title = await title_el.inner_text() if title_el else '未找到'
                    
                    # 获取价格
                    price_el = await item.query_selector('.a-price .a-offscreen, .a-price-whole')
                    price = await price_el.inner_text() if price_el else '未找到'
                    
                    # 获取评分
                    rating_el = await item.query_selector('.a-icon-alt, .a-star-small .a-icon-alt')
                    rating = await rating_el.inner_text() if rating_el else '未找到'
                    
                    # 获取评论数
                    reviews_el = await item.query_selector('.a-size-base.s-underline-text, [aria-label*="star"]')
                    reviews = await reviews_el.inner_text() if reviews_el else '未找到'
                    
                    # 获取排名
                    rank_el = await item.query_selector('.a-badge-supplementary-text')
                    best_seller_badge = await item.query_selector('[aria-label*="Best Seller"]')
                    
                    product = {
                        'asin': asin,
                        'title': title.strip(),
                        'price': price.strip() if price else '未找到',
                        'rating': rating.strip() if rating else '未找到',
                        'reviewCount': reviews.strip() if reviews else '未找到',
                        'isBestSeller': best_seller_badge is not None,
                        'index': i + 1
                    }
                    
                    products.append(product)
                    print(f"[{i+1}] {title[:50]}... - {price} - {rating}")
                    
                except Exception as e:
                    print(f"解析第{i+1}个结果时出错: {e}")
                    continue
            
            await browser.close()
            return products
    
    return asyncio.run(_search())


def get_competitor_details(asin, zip_code="10001"):
    """获取竞品详细信息"""
    async def _scrape():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                locale='en-US',
                extra_http_headers={
                    'Accept-Language': 'en-US,en;q=0.9'
                }
            )
            page = await context.new_page()
            
            await page.goto(f'https://www.amazon.com/dp/{asin}', 
                            wait_until='domcontentloaded', timeout=120000)
            await asyncio.sleep(5)
            
            # 设置邮编
            try:
                location_btn = await page.query_selector('#glow-ingress-line2')
                if location_btn:
                    await location_btn.click()
                    await asyncio.sleep(3)
                
                zip_input = await page.query_selector('#GLUXZipUpdateInput')
                if zip_input:
                    await zip_input.fill(zip_code)
                    await asyncio.sleep(1)
                    
                    submit_btn = await page.query_selector('#GLUXZipUpdate')
                    if submit_btn:
                        await submit_btn.click()
                        await asyncio.sleep(8)
            except:
                pass
            
            await page.reload(wait_until='domcontentloaded')
            await asyncio.sleep(3)
            
            # 获取详细信息
            title_el = await page.query_selector('#productTitle')
            name = await title_el.inner_text() if title_el else '未找到'
            
            # 价格
            price_el = await page.query_selector('.a-price .a-offscreen')
            price = await price_el.inner_text() if price_el else '未找到'
            
            # 评分
            rating_el = await page.query_selector('#acrPopover .a-icon-alt')
            rating = await rating_el.inner_text() if rating_el else '未找到'
            
            # 评论数
            reviews_el = await page.query_selector('#acrCustomerReviewText')
            reviews = await reviews_el.inner_text() if reviews_el else '未找到'
            
            # BSR排名
            bsr_el = await page.query_selector('#SalesRank .a-text-bold')
            bsr = await bsr_el.inner_text() if bsr_el else '未找到'
            
            # 预估销量
            estimate_el = await page.query_selector('[data-feature-name="savings"]')
            estimate = await estimate_el.inner_text() if estimate_el else '未找到'
            
            await browser.close()
            
            return {
                'asin': asin,
                'productName': name.strip()[:100],
                'price': price,
                'rating': rating,
                'reviewCount': reviews,
                'bsr': bsr,
                'parseTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    return asyncio.run(_scrape())


def generate_analysis_report(my_product, competitors):
    """
    生成对比分析报告
    my_product: {asin, productName, price, rating, reviewCount}
    competitors: [列表]
    """
    report = []
    report.append("=" * 60)
    report.append("Amazon竞品分析报告")
    report.append("=" * 60)
    report.append(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # 我的产品
    report.append("【自有产品】")
    report.append(f"  ASIN: {my_product.get('asin', 'N/A')}")
    report.append(f"  名称: {my_product.get('productName', '')[:60]}...")
    report.append(f"  价格: {my_product.get('price', 'N/A')}")
    report.append(f"  评分: {my_product.get('rating', 'N/A')}")
    report.append(f"  评论数: {my_product.get('reviewCount', 'N/A')}")
    report.append("")
    
    # 提取数值用于比较
    def extract_price(p):
        match = re.search(r'[\d,.]+', str(p))
        return float(match.group().replace(',', '')) if match else 0
    
    def extract_reviews(r):
        match = re.search(r'[\d,]+', str(r))
        return int(match.group().replace(',', '')) if match else 0
    
    my_price = extract_price(my_product.get('price', ''))
    my_reviews = extract_reviews(my_product.get('reviewCount', ''))
    my_rating = extract_price(my_product.get('rating', '0'))
    
    # 竞品列表
    report.append("【Top 3 竞品】")
    for i, comp in enumerate(competitors[:3], 1):
        report.append(f"")
        report.append(f"  竞品 {i}:")
        report.append(f"    ASIN: {comp.get('asin', 'N/A')}")
        report.append(f"    名称: {comp.get('title', 'N/A')[:60]}...")
        report.append(f"    价格: {comp.get('price', 'N/A')}")
        report.append(f"    评分: {comp.get('rating', 'N/A')}")
        report.append(f"    评论数: {comp.get('reviewCount', 'N/A')}")
        if comp.get('isBestSeller'):
            report.append(f"    标签: Best Seller")
    
    report.append("")
    report.append("=" * 60)
    report.append("【运营建议】")
    report.append("=" * 60)
    
    # 价格分析
    report.append("")
    report.append("1. 价格策略:")
    comp_prices = [extract_price(c.get('price', '0')) for c in competitors[:3] if extract_price(c.get('price', '0')) > 0]
    
    if my_price > 0 and comp_prices:
        avg_comp_price = sum(comp_prices) / len(comp_prices)
        if my_price > avg_comp_price * 1.2:
            report.append(f"   - 您的价格偏高(比竞品平均高{((my_price/avg_comp_price)-1)*100:.0f}%)")
            report.append(f"   - 建议: 考虑降价或突出产品差异化卖点")
        elif my_price < avg_comp_price * 0.8:
            report.append(f"   - 您的价格偏低(比竞品平均低{(1-(my_price/avg_comp_price))*100:.0f}%)")
            report.append(f"   - 建议: 可以适当提价提升利润")
        else:
            report.append(f"   - 您的价格处于合理区间(竞品均价${avg_comp_price:.2f})")
    
    # 评论数分析
    report.append("")
    report.append("2. 评论数策略:")
    comp_reviews = [extract_reviews(c.get('reviewCount', '0')) for c in competitors[:3]]
    
    if my_reviews > 0 and comp_reviews:
        max_comp_reviews = max(comp_reviews)
        if my_reviews < max_comp_reviews * 0.3:
            report.append(f"   - 竞品评论数领先较多(最高{max_comp_reviews}条 vs 您{my_reviews}条)")
            report.append(f"   - 建议: 加快评论积累，设置评论奖励计划")
        elif my_reviews < max_comp_reviews * 0.5:
            report.append(f"   - 竞品评论数较多(约{max_comp_reviews}条)")
            report.append(f"   - 建议: 保持稳定增长势头")
        else:
            report.append(f"   - 评论基础良好，继续保持")
    
    # 评分分析
    report.append("")
    report.append("3. 评分策略:")
    comp_ratings = [extract_price(c.get('rating', '0')) for c in competitors[:3] if extract_price(c.get('rating', '0')) > 0]
    
    if my_rating > 0 and comp_ratings:
        avg_rating = sum(comp_ratings) / len(comp_ratings)
        if my_rating < avg_rating - 0.3:
            report.append(f"   - 您的评分偏低({my_rating} vs 竞品平均{avg_rating:.1f})")
            report.append(f"   - 建议: 排查产品问题，提升产品质量")
        elif my_rating > avg_rating + 0.2:
            report.append(f"   - 您的评分优秀({my_rating} vs 竞品平均{avg_rating:.1f})")
            report.append(f"   - 建议: 利用高评分作为卖点宣传")
        else:
            report.append(f"   - 评分处于正常水平，继续维护")
    
    # 综合建议
    report.append("")
    report.append("4. 综合运营建议:")
    report.append("   - 持续监控竞品价格和评论变化")
    report.append("   - 关注差评内容，针对性改进产品")
    report.append("   - 大促节点(Prime Day/黑五)前调整定价策略")
    report.append("   - 引导用户留评，尤其是带图评论")
    
    return "\n".join(report)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python amazon_competitor_search.py <关键词>")
        print("示例: python amazon_competitor_search.py pool vacuum robot")
        sys.exit(1)
    
    keyword = sys.argv[1]
    print(f"正在搜索品类: {keyword}")
    
    # 搜索竞品
    competitors = search_competitors(keyword, max_results=10)
    
    if competitors:
        print(f"\n找到 {len(competitors)} 个竞品")
        
        # 获取前3竞品详细信息
        print("\n正在获取竞品详细信息...")
        top3_details = []
        for comp in competitors[:3]:
            asin = comp['asin']
            print(f"获取 {asin} 详情...")
            detail = get_competitor_details(asin)
            if detail and detail.get('productName') != '未找到':
                top3_details.append({
                    'asin': asin,
                    'title': comp['title'],
                    'price': detail.get('price', comp.get('price', 'N/A')),
                    'rating': detail.get('rating', comp.get('rating', 'N/A')),
                    'reviewCount': detail.get('reviewCount', comp.get('reviewCount', 'N/A')),
                    'isBestSeller': comp.get('isBestSeller', False)
                })
        
        # 生成报告
        my_product = {
            'asin': 'YOUR_ASIN',
            'productName': 'YOUR_PRODUCT',
            'price': 'N/A',
            'rating': 'N/A',
            'reviewCount': 'N/A'
        }
        
        report = generate_analysis_report(my_product, top3_details)
        print("\n" + report)
        
        # 保存报告
        report_file = f"competitor_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存: {report_file}")
    else:
        print("未找到竞品，请尝试其他关键词")
