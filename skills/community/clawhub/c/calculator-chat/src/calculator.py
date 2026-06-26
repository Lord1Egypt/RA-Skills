#!/usr/bin/env python3
"""
Calculator - 一个完整的计算器程序
支持鼠标点击按钮输入，进行加减乘除运算
"""

import sys
import os

os.environ.setdefault('DISPLAY', ':0')

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk


def safe_eval(expr):
    """
    安全地计算数学表达式
    只支持基本的四则运算
    """
    # 验证只包含安全字符
    safe_chars = set('0123456789+-*/.() ')
    if not all(c in safe_chars for c in expr):
        return None
    
    try:
        # 使用有限的安全操作
        # 创建一个受限的命名空间
        allowed_names = {
            'abs': abs,
            'min': min,
            'max': max,
            'pow': pow,
            'round': round,
        }
        
        # 使用 eval 但只允许数字和运算符
        result = eval(expr, {"__builtins__": {}}, allowed_names)
        return result
    except Exception:
        return None


class Calculator(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.current = ""
        self.result = 0
        self.operator = None
        self.new_number = True
        
    def on_click(self, button, value):
        """Handle button click"""
        if value == 'C':
            self.current = ""
            self.result = 0
            self.operator = None
            self.new_number = True
        elif value == '=':
            try:
                if self.operator and self.current:
                    expr = f"{self.result}{self.operator}{self.current}"
                    evaluated = safe_eval(expr)
                    if evaluated is not None:
                        self.result = evaluated
                        self.current = str(self.result)
                        self.new_number = True
                    else:
                        self.current = "Error"
            except:
                self.current = "Error"
        elif value in ['+', '-', '*', '/']:
            try:
                if self.current:
                    if self.operator:
                        expr = f"{self.result}{self.operator}{self.current}"
                        evaluated = safe_eval(expr)
                        if evaluated is not None:
                            self.result = evaluated
                        else:
                            self.current = "Error"
                            return
                    else:
                        evaluated = safe_eval(self.current)
                        if evaluated is not None:
                            self.result = evaluated
                        else:
                            self.current = "Error"
                            return
                    self.current = str(self.result)
                self.operator = value
                self.new_number = True
            except:
                self.current = "Error"
        else:
            if self.new_number:
                self.current = value
                self.new_number = False
            else:
                self.current += value
        
        # Update display
        self.display.set_text(self.current or "0")
        
    def create_buttons(self):
        """Create calculator buttons"""
        buttons = [
            ('C', '7', '8', '9', '/'),
            ('', '4', '5', '6', '*'),
            ('', '1', '2', '3', '-'),
            ('=', '0', '.', '', '+'),
        ]
        
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        
        for row, cols in enumerate(buttons):
            for col, val in enumerate(cols):
                if val == '':
                    continue
                    
                btn = Gtk.Button(label=val)
                btn.set_hexpand(True)
                btn.set_vexpand(True)
                
                # Style buttons
                btn.add_css_class("calc-btn")
                if val in ['+', '-', '*', '/', '=']:
                    btn.add_css_class("operator")
                elif val == 'C':
                    btn.add_css_class("clear")
                else:
                    btn.add_css_class("number")
                
                btn.connect("clicked", self.on_click, val)
                grid.attach(btn, col, row, 1, 1)
        
        return grid
    
    def create_display(self):
        """Create display screen"""
        self.display = Gtk.Label()
        self.display.set_text("0")
        self.display.set_halign(Gtk.Align.END)
        self.display.set_valign(Gtk.Align.CENTER)
        self.display.set_hexpand(True)
        self.display.set_vexpand(True)
        
        # Display container
        box = Gtk.Box()
        box.set_homogeneous(True)
        box.add_css_class("display")
        box.append(self.display)
        
        return box
    
    def do_activate(self):
        """Create window"""
        win = Gtk.ApplicationWindow(application=self)
        win.set_title("🧮 Calculator")
        win.set_default_size(350, 450)
        win.set_resizable(False)
        
        # Main box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        
        # Add display
        vbox.append(self.create_display())
        
        # Add buttons
        vbox.append(self.create_buttons())
        
        win.set_child(vbox)
        
        # Apply CSS
        self.apply_css()
        
        win.present()
    
    def apply_css(self):
        """Apply calculator styling"""
        css = """
            .display {
                background-color: #1e1e1e;
                border-radius: 10px;
                padding: 20px;
            }
            .display label {
                color: white;
                font-size: 36px;
            }
            .calc-btn {
                font-size: 24px;
                border-radius: 8px;
                padding: 15px;
            }
            .calc-btn.number {
                background-color: #3d3d3d;
                color: white;
            }
            .calc-btn.number:hover {
                background-color: #4d4d4d;
            }
            .calc-btn.operator {
                background-color: #ff9500;
                color: white;
            }
            .calc-btn.operator:hover {
                background-color: #ffaa33;
            }
            .calc-btn.clear {
                background-color: #ff3b30;
                color: white;
            }
            .calc-btn.clear:hover {
                background-color: #ff5545;
            }
            window {
                background-color: #2d2d2d;
            }
        """
        provider = Gtk.CssProvider()
        provider.load_from_string(css)
        
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display, provider, 600
        )


def run():
    app = Calculator()
    app.run()


if __name__ == '__main__':
    run()
