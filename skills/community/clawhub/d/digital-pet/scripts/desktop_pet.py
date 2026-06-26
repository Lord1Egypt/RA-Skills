#!/usr/bin/env python3
"""
数字宠物 - Desktop Pet
一个可爱的 3D 拉布布宠物，会跟随鼠标在桌面上移动
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QSystemTrayIcon,
    QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import (
    Qt, QTimer, QPoint, QUrl, pyqtSignal, QObject
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon, QCursor


class PetBridge(QObject):
    """用于 JavaScript 和 Python 通信的桥梁"""
    mouseMoveSignal = pyqtSignal(float, float)
    clickSignal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
    
    def moveToMouse(self, x, y):
        """JavaScript 调用：移动宠物到指定位置"""
        if self.parent:
            self.parent.movePet(int(x), int(y))
    
    def log(self, message):
        """JavaScript 调用：打印日志"""
        print(f"[JS] {message}")


class DigitalPet(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 窗口设置
        self.setWindowTitle("数字宠物 - Digital Pet")
        self.setGeometry(100, 100, 400, 500)
        
        # 无边框窗口，始终置顶
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # 透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 鼠标跟踪
        self.setMouseTracking(True)
        
        # 拖动相关
        self.dragging = False
        self.drag_position = None
        
        # 跟随模式
        self.follow_mode = True
        self.offset_x = 50  # 宠物相对于鼠标的偏移
        self.offset_y = -200
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 布局
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建 WebView
        self.webview = QWebEngineView()
        self.webview.setMouseTracking(True)
        
        # 设置透明背景
        self.webview.page().setBackgroundColor(Qt.transparent)
        
        # 设置 WebChannel
        self.channel = QWebChannel()
        self.bridge = PetBridge(self)
        self.channel.registerObject("pybridge", self.bridge)
        self.webview.page().setWebChannel(self.channel)
        
        # 加载 HTML 文件
        html_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "pet_widget.html"
        )
        self.webview.load(QUrl.fromLocalFile(html_path))
        
        layout.addWidget(self.webview)
        
        # 创建控制按钮（可隐藏）
        self.createControlButtons(layout)
        
        # 创建系统托盘
        self.createSystemTray()
        
        # 定时更新位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePosition)
        self.timer.start(16)  # 60 FPS
        
        # 显示窗口
        self.show()
        
        print("✅ 数字宠物已启动！")
        print("🖱️ 宠物会跟随鼠标移动")
        print("👆 拖拽可以手动移动位置")
        print("🖱️ 右键点击打开菜单")
    
    def createControlButtons(self, layout):
        """创建控制按钮"""
        button_layout = QHBoxLayout()
        
        # 关闭按钮
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 100, 100, 0.8);
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 50, 50, 0.9);
            }
        """)
        close_btn.clicked.connect(self.hide)
        button_layout.addWidget(close_btn)
        
        # 设置按钮
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(30, 30)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(100, 100, 255, 0.8);
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 255, 0.9);
            }
        """)
        settings_btn.clicked.connect(self.showSettings)
        button_layout.addWidget(settings_btn)
        
        # 切换模式按钮
        mode_btn = QPushButton("🎯")
        mode_btn.setFixedSize(30, 30)
        mode_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(100, 255, 100, 0.8);
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(50, 255, 50, 0.9);
            }
        """)
        mode_btn.clicked.connect(self.toggleMode)
        button_layout.addWidget(mode_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def createSystemTray(self):
        """创建系统托盘图标"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # 创建一个简单的图标（如果没有图标文件）
        from PyQt5.QtGui import QPixmap, QPainter, QColor
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(100, 200, 100))
        painter.drawEllipse(8, 8, 48, 48)
        painter.end()
        
        self.tray_icon.setIcon(QIcon(pixmap))
        self.tray_icon.setToolTip("数字宠物 - Digital Pet")
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.showSettings)
        tray_menu.addAction(settings_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quitApp)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.trayIconActivated)
        
        self.tray_icon.show()
    
    def trayIconActivated(self, reason):
        """托盘图标被激活"""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
    
    def updatePosition(self):
        """更新宠物位置"""
        if not self.follow_mode or self.dragging:
            return
        
        # 获取鼠标位置
        cursor_pos = QCursor.pos()
        
        # 计算目标位置（鼠标右下方）
        target_x = cursor_pos.x() + self.offset_x
        target_y = cursor_pos.y() + self.offset_y
        
        # 平滑移动
        current_pos = self.pos()
        new_x = current_pos.x() + (target_x - current_pos.x()) * 0.1
        new_y = current_pos.y() + (target_y - current_pos.y()) * 0.1
        
        # 边界检查
        screen = QApplication.primaryScreen().geometry()
        new_x = max(0, min(new_x, screen.width() - self.width()))
        new_y = max(0, min(new_y, screen.height() - self.height()))
        
        self.move(int(new_x), int(new_y))
    
    def movePet(self, x, y):
        """移动宠物到指定位置"""
        self.move(x, y)
    
    def toggleMode(self):
        """切换跟随/固定模式"""
        self.follow_mode = not self.follow_mode
        mode = "跟随模式" if self.follow_mode else "固定模式"
        print(f"🎯 切换到：{mode}")
        
        # 通过 JavaScript 更新状态
        self.webview.page().runJavaScript(
            f"window.setFollowMode && window.setFollowMode({str(self.follow_mode).lower()});"
        )
    
    def showSettings(self):
        """显示设置对话框"""
        QMessageBox.information(
            self,
            "设置",
            "数字宠物设置\n\n"
            "🖱️ 跟随模式：宠物会跟随鼠标移动\n"
            "👆 拖拽模式：可以手动拖动宠物\n\n"
            "快捷键：\n"
            "- 双击托盘图标：显示/隐藏\n"
            "- 右键托盘图标：菜单"
        )
    
    def quitApp(self):
        """退出应用程序"""
        self.tray_icon.hide()
        QApplication.quit()
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.RightButton:
            # 右键显示菜单
            pass
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def closeEvent(self, event):
        """关闭事件"""
        event.ignore()
        self.hide()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 检查 PyQt5 WebEngine
    try:
        from PyQt5.QtWebEngineWidgets import QWebEngineView
    except ImportError:
        print("❌ 请先安装 PyQt5 WebEngine:")
        print("   pip install PyQt5 PyQtWebEngine")
        sys.exit(1)
    
    pet = DigitalPet()
    
    print("\n🎉 数字宠物已就绪！")
    print("📝 提示：")
    print("   - 宠物会跟随你的鼠标移动")
    print("   - 可以拖拽宠物到任意位置")
    print("   - 点击系统托盘图标可以隐藏/显示")
    print("   - 右键托盘图标查看更多选项")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
