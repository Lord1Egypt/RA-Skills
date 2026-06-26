import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        # ====================== 1. 抓取当天涨幅Top10（增强额外信息） ======================
        print("正在从同花顺抓取当天A股涨幅Top10...")
        await page.goto("https://data.10jqka.com.cn/market/zdfph/", timeout=60000)
        await page.wait_for_timeout(6000)  # 等待表格完全加载

        top10 = []
        rows = await page.locator("table tr").all()
        for row in rows[1:]:  # 跳过表头
            try:
                cells = await row.locator("td").all_inner_texts()
                if len(cells) >= 5 and cells[1].strip().isdigit():  # 代码是数字
                    code = cells[1].strip()
                    name = cells[2].strip()
                    price = cells[3].strip()
                    change = cells[4].strip().replace('%', '')

                    # === 额外有用信息（根据同花顺实际表格列安全提取）===
                    volume = cells[6].strip() if len(cells) > 6 else "—"
                    turnover = cells[5].strip() if len(cells) > 5 else "—"   # 换手率
                    amplitude = cells[8].strip() if len(cells) > 8 else "—"
                    inflow = cells[6].strip() if len(cells) > 6 else "—"     # 资金净流入

                    top10.append({
                        "代码": code,
                        "名称": name,
                        "最新价": price,
                        "涨跌幅": change,
                        "成交量(手)": volume,
                        "换手率(%)": turnover,
                        "振幅(%)": amplitude,
                        "资金净流入": inflow
                    })
                    if len(top10) >= 10:
                        break
            except:
                continue

        df_top10 = pd.DataFrame(top10)
        print("\n=== 当天涨幅 Top 10（已带额外字段） ===")
        print(df_top10.to_string(index=False))

        await browser.close()


asyncio.run(main())