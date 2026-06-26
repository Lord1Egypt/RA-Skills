"""
Pywinauto Windows App Automation Demo
Pywinauto Windows 应用自动化示例

Demonstrates controlling native Windows applications.
演示控制 Windows 原生应用。

Installation / 安装:
    pip install pywinauto

Usage / 使用:
    python pywinauto_demo.py --app notepad --action <action>
"""

import argparse
import time
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError


def start_app(app_name: str) -> Application:
    """Start a Windows application / 启动 Windows 应用
    
    Args:
        app_name: Application name or path / 应用名称或路径
        
    Common apps / 常见应用:
        notepad, calc, mspaint, explorer, winword, excel
    """
    print(f"Starting application: {app_name}")
    app = Application().start(f'{app_name}.exe')
    time.sleep(1)  # Wait for app to start
    return app


def connect_app(title: str) -> Application:
    """Connect to existing application / 连接到已有应用
    
    Args:
        title: Window title (partial match) / 窗口标题（部分匹配）
    """
    print(f"Connecting to window: {title}")
    app = Application().connect(title_re=f".*{title}.*")
    return app


def get_window(app: Application, title_pattern: str = None):
    """Get main window / 获取主窗口
    
    Args:
        app: Application instance / 应用实例
        title_pattern: Window title pattern / 窗口标题模式
    """
    if title_pattern:
        return app.window(title_re=f".*{title_pattern}.*")
    return app.top_window()


def type_in_notepad(text: str):
    """Demo: Type text in Notepad / 示例：在记事本中输入文本"""
    print(f"\n=== Notepad Demo / 记事本示例 ===")
    
    # Start Notepad / 启动记事本
    app = start_app('notepad')
    win = get_window(app, 'Notepad')
    
    # Type text / 输入文本
    print(f"Typing: {text}")
    win.Edit.type_keys(text, with_spaces=True)
    
    # Wait to see result / 等待查看结果
    time.sleep(2)
    
    # Close without saving / 不保存关闭
    win.close()
    try:
        # Handle "Save changes?" dialog / 处理"是否保存"对话框
        app.window(title='Notepad').DontSave.click()
    except:
        pass
    
    print("Done.")


def calculator_demo():
    """Demo: Use Calculator / 示例：使用计算器"""
    print(f"\n=== Calculator Demo / 计算器示例 ===")
    
    # Start Calculator / 启动计算器
    app = start_app('calc')
    time.sleep(2)
    
    win = get_window(app)
    
    # Click buttons / 点击按钮
    # Note: Button names may vary by Windows version / 注意：按钮名称可能因 Windows 版本不同
    try:
        win.window(title='One').click()
        win.window(title='Plus').click()
        win.window(title='Two').click()
        win.window(title='Equals').click()
        print("Calculated: 1 + 2")
    except ElementNotFoundError as e:
        print(f"Button not found: {e}")
        print("Calculator UI varies by Windows version")
    
    time.sleep(2)
    win.close()
    print("Done.")


def list_controls(app_name: str):
    """List all controls in an app / 列出应用中的所有控件
    
    Args:
        app_name: Application name / 应用名称
    """
    print(f"\n=== Listing controls in {app_name} ===")
    
    app = start_app(app_name)
    time.sleep(1)
    
    win = app.top_window()
    
    # Print control identifiers / 打印控件标识符
    print("\nControl identifiers:")
    win.print_control_identifiers()
    
    win.close()


def main():
    parser = argparse.ArgumentParser(
        description='Pywinauto Windows App Automation / Pywinauto Windows 应用自动化'
    )
    parser.add_argument('--app', default='notepad',
                       help='Application name (notepad, calc, mspaint) / 应用名称')
    parser.add_argument('--action', default='demo',
                       choices=['demo', 'list', 'type', 'calc'],
                       help='Action to perform / 要执行的操作')
    parser.add_argument('--text', default='Hello from pywinauto!\n你好，pywinauto！',
                       help='Text to type / 要输入的文本')
    
    args = parser.parse_args()
    
    if args.action == 'demo':
        type_in_notepad(args.text)
    elif args.action == 'type':
        type_in_notepad(args.text)
    elif args.action == 'calc':
        calculator_demo()
    elif args.action == 'list':
        list_controls(args.app)


if __name__ == '__main__':
    main()
