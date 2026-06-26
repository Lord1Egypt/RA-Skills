#!/usr/bin/env python3
"""
番茄后台评论自动审核脚本 - 支持刷新和视频评论
"""
from playwright.sync_api import sync_playwright
import time

def auto_review(loop_count=50):
    with sync_playwright() as p:
        print("连接浏览器...")
        browser = p.chromium.connect_over_cdp("http://localhost:18800")
        context = browser.contexts[0]
        
        # 找到审核页面
        target_page = None
        for page in context.pages:
            if "dynamicCommentVerity" in page.url:
                target_page = page
                break
        
        if not target_page:
            print("未找到审核页面，请先打开评论审核页面")
            return
        
        print(f"审核页面: {target_page.url}")
        
        total_reviewed = 0
        
        for loop in range(loop_count):
            # 刷新页面获取新数据
            print(f"\n--- 第{loop+1}轮 ---")
            target_page.reload()
            target_page.wait_for_load_state("networkidle")
            time.sleep(2)
            
            # 检查是否有数据
            try:
                empty = target_page.query_selector('.el-table__empty-block')
                if empty:
                    print("暂无数据，3秒后重试...")
                    time.sleep(3)
                    continue
            except:
                pass
            
            # 审核当前页面的评论
            reviewed_this_round = 0
            
            while True:
                # 找操作列的通过按钮
                result = target_page.evaluate('''() => {
                    const wrapper = document.querySelector('.el-table__body-wrapper');
                    if (!wrapper) return {error: 'no wrapper'};
                    
                    const tbody = wrapper.querySelector('.el-table__body tbody');
                    if (!tbody) return {error: 'no tbody'};
                    
                    const rows = tbody.querySelectorAll('tr.el-table__row');
                    if (rows.length === 0) return {error: 'no rows'};
                    
                    const row = rows[0];
                    const cells = row.querySelectorAll('td.el-table__cell');
                    const lastCell = cells[cells.length - 1];
                    const btnGroup = lastCell.querySelector('.cell');
                    if (!btnGroup) return {error: 'no btnGroup'};
                    
                    const buttons = btnGroup.querySelectorAll('.el-button');
                    let passed = false;
                    buttons.forEach(btn => {
                        const text = btn.innerText.trim();
                        if (text === '通过' && !btn.classList.contains('is-disabled')) {
                            btn.click();
                            passed = true;
                        }
                    });
                    
                    return {passed: passed};
                }''')
                
                if result.get('error'):
                    if 'no rows' in str(result.get('error', '')):
                        print("本页审核完成")
                        break
                    print(f"等待数据: {result}")
                    time.sleep(2)
                    continue
                
                if result.get('passed'):
                    total_reviewed += 1
                    reviewed_this_round += 1
                    print(f"已审核: {total_reviewed}条 (本轮: {reviewed_this_round})")
                    time.sleep(1)
                else:
                    break
            
            # 本轮结束，检查是否还有数据
            if reviewed_this_round == 0:
                print("没有更多数据，3秒后刷新...")
                time.sleep(3)
        
        print(f"\n审核完成! 共审核 {total_reviewed} 条评论")
        browser.close()

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    auto_review(count)
