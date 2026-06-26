#!/usr/bin/env python3
"""
DeepSeek Web Query - 使用 Playwright 控制浏览器访问 DeepSeek 网页版进行查询
"""

import sys
import json
import os
from pathlib import Path

# Playwright 导入
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("错误：需要安装 Playwright")
    print("请运行: pip install playwright")
    print("然后运行: playwright install chromium")
    sys.exit(1)

# 配置
DEEPSEEK_URL = "https://chat.deepseek.com/"
AUTH_FILE = Path(__file__).parent / "deepseek_auth.json"
BROWSER_STATE_FILE = Path(__file__).parent / ".browser_state"


def get_browser_state():
    """获取浏览器状态文件路径"""
    return BROWSER_STATE_FILE


def is_browser_running():
    """检查浏览器是否已在运行"""
    state_file = get_browser_state()
    if not state_file.exists():
        return False
    try:
        with open(state_file, 'r') as f:
            state = json.load(f)
        # 简单检查：如果状态文件存在且未过期（1小时），认为浏览器在运行
        import time
        if time.time() - state.get('timestamp', 0) < 3600:
            return True
    except:
        pass
    return False


def save_browser_state(context=None):
    """保存浏览器状态"""
    state_file = get_browser_state()
    import time
    state = {
        'timestamp': time.time(),
        'has_context': context is not None
    }
    with open(state_file, 'w') as f:
        json.dump(state, f)


def load_auth_state():
    """加载保存的登录状态"""
    if AUTH_FILE.exists():
        try:
            with open(AUTH_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return None


def query_deepseek(question: str, headless: bool = False):
    """
    使用 DeepSeek 网页版进行查询
    
    Args:
        question: 查询问题
        headless: 是否使用无头模式（默认 False，方便调试）
    
    Returns:
        dict: 包含回答内容和元数据
    """
    result = {
        'success': False,
        'question': question,
        'optimized_question': None,
        'answer': None,
        'error': None
    }
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=headless)
        
        # 创建新页面或使用现有上下文
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        
        page = context.new_page()
        
        try:
            print(f"🌐 正在加载 DeepSeek...")
            page.goto(DEEPSEEK_URL, wait_until="networkidle", timeout=30000)
            
            # 等待页面加载完成
            page.wait_for_load_state("networkidle")
            
            # 检查是否需要登录
            # DeepSeek 的输入框选择器（可能需要根据实际页面调整）
            input_selector = 'textarea[placeholder*="发送消息"], textarea[placeholder*="Message"], .chat-input textarea, [contenteditable="true"]'
            
            try:
                # 等待输入框出现
                page.wait_for_selector(input_selector, timeout=10000)
                print("✅ DeepSeek 已加载！")
            except PlaywrightTimeout:
                # 可能需要登录
                print("⚠️ 可能需要登录 DeepSeek")
                print("请先在浏览器中完成登录，然后重新运行")
                result['error'] = "需要登录 DeepSeek"
                
                # 保持浏览器打开供用户登录
                if not headless:
                    print("浏览器将保持打开 60 秒...")
                    page.wait_for_timeout(60000)
                
                browser.close()
                return result
            
            # 优化问题（简单的优化逻辑）
            optimized = optimize_question(question)
            result['optimized_question'] = optimized
            print(f"\n📝 原始问题: {question}")
            if optimized != question:
                print(f"✨ 优化后: {optimized}")
            
            # 1. 检查深度思考按钮状态，如果未选中则点击
            print(f"\n🔍 检查深度思考按钮状态...")
            deep_think_selector = 'button:has-text("深度思考"), button[class*="deep-thinking"], button[class*="reasoning"]'
            try:
                deep_think_button = page.wait_for_selector(deep_think_selector, timeout=5000)
                # 检查按钮状态（是否已选中）
                is_active = deep_think_button.get_attribute("data-active") == "true" or \
                           "active" in (deep_think_button.get_attribute("class") or "")
                
                if not is_active:
                    print("🔄 启用深度思考模式...")
                    deep_think_button.click()
                    page.wait_for_timeout(1000)  # 等待状态更新
                else:
                    print("✅ 深度思考模式已启用")
            except Exception as e:
                print(f"⚠️ 深度思考按钮处理异常: {e}")
                # 继续执行，不影响主要流程
            
            # 2. 输入问题
            print(f"\n🔍 正在发送查询...")
            
            # 确保焦点在输入框
            try:
                input_element = page.wait_for_selector(input_selector, timeout=5000)
                input_element.click()  # 点击输入框获取焦点
                page.wait_for_timeout(500)
                
                # 清空输入框（如果有内容）
                input_element.fill("")
                page.wait_for_timeout(500)
                
                # 输入问题
                input_element.fill(optimized)
                page.wait_for_timeout(500)
            except Exception as e:
                print(f"输入失败: {e}")
                result['error'] = f"无法输入问题: {e}"
                browser.close()
                return result
            
            # 3. 发送消息（按 Enter）
            page.keyboard.press("Enter")
            
            # 等待响应
            print("⏳ 等待 DeepSeek 回答...")
            
            # 等待响应完成
            page.wait_for_timeout(3000)  # 初始等待
            
            # 检测深度思考模式是否启用（R1 模式）
            thinking_selector = '.thinking, .reasoning, [class*="think"]'
            answer_selector = '.message-content, .chat-message, [class*="message"]'
            
            # 等待一段时间让回答生成
            max_wait = 90  # 最大等待 90 秒
            waited = 0
            while waited < max_wait:
                page.wait_for_timeout(1000)
                waited += 1
                
                # 检查是否还在思考/生成中
                try:
                    stop_button = page.query_selector('button:has-text("停止"), button:has-text("Stop")')
                    if stop_button:
                        continue  # 还在生成中
                except:
                    pass
                
                # 检查是否有新内容
                try:
                    messages = page.query_selector_all(answer_selector)
                    if len(messages) > 0:
                        # 获取最后一条消息
                        last_message = messages[-1]
                        text = last_message.inner_text()
                        if text and len(text) > 10:
                            break
                except:
                    pass
            
            # 4. 提取回答 - 使用拷贝按钮获取 Markdown 格式
            print("✅ 获取到回答，尝试通过拷贝按钮提取...")
            
            try:
                # 查找拷贝按钮（通常在消息右上角）
                copy_button_selector = 'button[title*="复制"], button[title*="Copy"], button[class*="copy"], button:has(svg[class*="copy"])'
                
                # 等待拷贝按钮出现
                page.wait_for_selector(copy_button_selector, timeout=10000)
                
                # 查找所有拷贝按钮，点击最后一个（最新回答的拷贝按钮）
                copy_buttons = page.query_selector_all(copy_button_selector)
                if copy_buttons:
                    last_copy_button = copy_buttons[-1]
                    last_copy_button.click()
                    print("📋 已点击拷贝按钮，Markdown 内容已复制到剪贴板")
                    
                    # 从剪贴板获取内容
                    page.wait_for_timeout(1000)  # 等待复制完成
                    
                    # 使用 evaluate 获取剪贴板内容
                    clipboard_content = page.evaluate("""
                        async () => {
                            try {
                                return await navigator.clipboard.readText();
                            } catch (err) {
                                console.error('读取剪贴板失败:', err);
                                return null;
                            }
                        }
                    """)
                    
                    if clipboard_content:
                        result['answer'] = clipboard_content.strip()
                        result['success'] = True
                        print("✅ 成功从剪贴板获取 Markdown 内容")
                    else:
                        # 如果剪贴板获取失败，尝试直接提取页面内容
                        print("⚠️ 剪贴板获取失败，尝试直接提取页面内容...")
                        messages = page.query_selector_all(answer_selector)
                        if messages:
                            last_message = messages[-1]
                            answer_text = last_message.inner_text()
                            result['answer'] = answer_text.strip()
                            result['success'] = True
                        else:
                            result['answer'] = page.inner_text('body')
                            result['success'] = True
                else:
                    print("⚠️ 未找到拷贝按钮，直接提取页面内容...")
                    messages = page.query_selector_all(answer_selector)
                    if messages:
                        last_message = messages[-1]
                        answer_text = last_message.inner_text()
                        result['answer'] = answer_text.strip()
                        result['success'] = True
                    else:
                        result['answer'] = page.inner_text('body')
                        result['success'] = True
                        
            except Exception as e:
                print(f"⚠️ 通过拷贝按钮提取失败: {e}")
                # 备选方案：直接提取页面内容
                try:
                    messages = page.query_selector_all(answer_selector)
                    if messages:
                        last_message = messages[-1]
                        answer_text = last_message.inner_text()
                        result['answer'] = answer_text.strip()
                        result['success'] = True
                    else:
                        result['answer'] = page.inner_text('body')
                        result['success'] = True
                except Exception as e2:
                    print(f"提取回答失败: {e2}")
                    result['error'] = f"提取回答失败: {e2}"
            
            # 保存浏览器状态
            save_browser_state(context)
            
            # 保持浏览器打开（不关闭）
            print("\n💡 浏览器保持打开状态，可供后续查询使用")
            print("   如需关闭，请手动关闭浏览器窗口或重启 OpenClaw")
            
            # 给浏览器一点时间稳定
            page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"❌ 错误: {e}")
            result['error'] = str(e)
        
        # 注意：这里不关闭浏览器，保持会话
        # browser.close()  # 注释掉，保持浏览器打开
    
    return result


def optimize_question(question: str) -> str:
    """
    优化用户提问，使其更清晰、具体
    
    简单的优化规则：
    1. 处理 ds: 或 ds：前缀（移除）
    2. 去除多余空格
    3. 对于非 ds: 开头的短问题，添加提示
    4. 对于模糊问题，引导更具体的提问
    """
    question = question.strip()
    
    # 处理 ds: 或 ds：前缀
    if question.startswith("ds:") or question.startswith("ds："):
        # 移除前缀
        if question.startswith("ds:"):
            question = question[3:].strip()
        else:  # ds：
            question = question[3:].strip()
        # ds: 前缀的问题不添加额外提示，保持原样
        return question
    
    # 如果问题太短且不是 ds: 前缀，添加提示
    if len(question) < 10:
        question = f"请详细介绍：{question}"
    
    # 如果是代码相关问题但没有指定语言，添加提示
    code_keywords = ['代码', '编程', '函数', 'bug', '错误', '报错', 'python', 'java', 'javascript']
    if any(kw in question.lower() for kw in code_keywords):
        if not any(lang in question.lower() for lang in ['用python', '用java', '用js', '用javascript', '用c++', '用go']):
            # 不强制添加，保持原问题
            pass
    
    return question


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python deepseek_query.py \"你的查询问题\"")
        print("示例: python deepseek_query.py \"Python 3.12 新特性\"")
        sys.exit(1)
    
    question = sys.argv[1]
    
    # 检查命令行参数
    headless = '--headless' in sys.argv
    
    print("=" * 50)
    print("🚀 DeepSeek Web Query")
    print("=" * 50)
    
    # 执行查询
    result = query_deepseek(question, headless=headless)
    
    # 输出结果
    print("\n" + "=" * 50)
    print("📊 查询结果")
    print("=" * 50)
    
    if result['success']:
        print(f"\n❓ 问题: {result['question']}")
        if result['optimized_question'] != result['question']:
            print(f"✨ 优化后: {result['optimized_question']}")
        print(f"\n💬 回答:\n{result['answer']}")
        
        # 同时输出 JSON 格式供程序解析
        print("\n" + "-" * 50)
        print("JSON_OUTPUT:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 查询失败: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
