#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12306 购票自动化客户端
"""

import os, time, json
from typing import Optional, List, Dict
from playwright.sync_api import sync_playwright, Page, Browser


class Railway12306Client:
    """12306 购票自动化客户端"""

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        cookie_file: str = "12306_cookies.json",
        headless: bool = False,
    ):
        self.username = username or os.getenv("RAILWAY_12306_USERNAME")
        self.password = password or os.getenv("RAILWAY_12306_PASSWORD")
        self.cookie_file = cookie_file
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.base_url = "https://www.12306.cn"

    def start(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=self.headless)
        context = self.browser.new_context(viewport={"width": 1920, "height": 1080})
        self.page = context.new_page()
        return self

    def load_cookies(self) -> bool:
        if not os.path.exists(self.cookie_file):
            return False
        try:
            with open(self.cookie_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            self.page.context.add_cookies(cookies)
            return True
        except:
            return False

    def save_cookies(self):
        try:
            with open(self.cookie_file, "w", encoding="utf-8") as f:
                json.dump(self.page.context.cookies(), f, ensure_ascii=False, indent=2)
        except:
            pass

    def login(self) -> bool:
        if self.load_cookies():
            self.page.goto(self.base_url)
            time.sleep(3)
            if self.is_logged_in():
                return True

        self.page.goto(f"{self.base_url}/index/login")
        time.sleep(5)
        self.save_cookies()
        return self.is_logged_in()

    def is_logged_in(self) -> bool:
        try:
            return ".user-info" in self.page.content()
        except:
            return False

    def search_tickets(
        self, from_station: str, to_station: str, date: str
    ) -> List[Dict]:
        """查询车票"""
        try:
            self.page.goto(f"{self.base_url}/index/queryTicket")
            time.sleep(3)

            # 填写查询条件
            from_input = self.page.query_selector('input[placeholder*="出发"]')
            to_input = self.page.query_selector('input[placeholder*="到达"]')
            date_input = self.page.query_selector('input[placeholder*="日期"]')

            if from_input and to_input and date_input:
                from_input.fill(from_station)
                to_input.fill(to_station)
                date_input.fill(date)

                # 点击查询
                search_btn = self.page.query_selector('button:has-text("查询")')
                if search_btn:
                    search_btn.click()
                    time.sleep(5)

                    # 获取结果
                    tickets = []
                    rows = self.page.query_selector_all(".ticket-row")
                    for row in rows[:10]:
                        try:
                            train = row.query_selector(".train-no").inner_text()
                            time_dep = row.query_selector(".dep-time").inner_text()
                            time_arr = row.query_selector(".arr-time").inner_text()
                            tickets.append(
                                {
                                    "train": train,
                                    "departure": time_dep,
                                    "arrival": time_arr,
                                }
                            )
                        except:
                            continue

                    return tickets

            return []
        except Exception as e:
            print(f"查询失败：{e}")
            return []

    def close(self):
        if self.browser:
            self.browser.close()


def main():
    print("12306 购票自动化")
    client = Railway12306Client(headless=False)
    client.start()
    try:
        if client.login():
            print("✅ 登录成功")
        else:
            print("❌ 登录失败")
    finally:
        client.close()


if __name__ == "__main__":
    main()
