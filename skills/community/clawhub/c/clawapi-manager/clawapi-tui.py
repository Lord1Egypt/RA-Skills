#!/usr/bin/env python3
"""
ClawAPI Manager TUI - 完整版
基于 Textual 的配置管理面板
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Button, Static, TabbedContent, TabPane, 
    DataTable, Input, Label, Select, Switch
)
from textual.binding import Binding
from textual.screen import ModalScreen
import sys
import os

# 添加 lib 目录
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from config_manager import ClawAPIConfigManager


class AddProviderScreen(ModalScreen):
    """添加 Provider 对话框"""
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label("Add Provider", id="dialog-title")
            yield Input(placeholder="Provider name", id="provider-name")
            yield Input(placeholder="Base URL", id="provider-url")
            yield Input(placeholder="API Key", password=True, id="provider-key")
            with Horizontal(classes="button-row"):
                yield Button("Add", variant="primary", id="add-btn")
                yield Button("Cancel", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-btn":
            name = self.query_one("#provider-name", Input).value
            url = self.query_one("#provider-url", Input).value
            key = self.query_one("#provider-key", Input).value
            
            if name and url and key:
                self.dismiss((name, url, key))
            else:
                self.app.notify("All fields required!", severity="error")
        else:
            self.dismiss(None)


class AddChannelScreen(ModalScreen):
    """添加 Channel 对话框"""
    
    CHANNEL_TYPES = [
        ("QQ Bot", "qqbot"),
        ("WeChat Work", "wecom"),
        ("Feishu", "feishu"),
        ("DingTalk", "dingtalk"),
        ("Telegram", "telegram"),
        ("Discord", "discord"),
        ("Slack", "slack"),
    ]
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label("Add Channel", id="dialog-title")
            yield Input(placeholder="Channel name", id="channel-name")
            yield Select(
                options=[(name, value) for name, value in self.CHANNEL_TYPES],
                prompt="Select channel type",
                id="channel-type"
            )
            yield Input(placeholder="App ID / Bot Token", id="channel-token")
            with Horizontal(classes="button-row"):
                yield Button("Add", variant="primary", id="add-btn")
                yield Button("Cancel", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-btn":
            name = self.query_one("#channel-name", Input).value
            channel_type = self.query_one("#channel-type", Select).value
            token = self.query_one("#channel-token", Input).value
            
            if name and channel_type and token:
                self.dismiss((name, channel_type, token))
            else:
                self.app.notify("All fields required!", severity="error")
        else:
            self.dismiss(None)


class ClawAPITUI(App):
    """ClawAPI Manager TUI"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #status-bar {
        dock: top;
        height: 3;
        background: $primary;
        color: $text;
        padding: 1;
    }
    
    DataTable {
        height: 100%;
    }
    
    .button-row {
        height: 3;
        padding: 1;
    }
    
    Button {
        margin: 0 1;
    }
    
    #dialog {
        width: 60;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1;
    }
    
    #dialog-title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }
    
    Input {
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("ctrl+s", "save", "Save"),
    ]
    
    def __init__(self):
        super().__init__()
        self.manager = ClawAPIConfigManager()
    
    def compose(self) -> ComposeResult:
        """创建界面"""
        yield Header()
        
        # 状态栏
        yield Static(id="status-bar", markup=True)
        
        # 主内容区（三个标签页）
        with TabbedContent():
            # Models 标签页
            with TabPane("Models", id="models-tab"):
                yield DataTable(id="models-table", cursor_type="row")
                with Horizontal(classes="button-row"):
                    yield Button("Add Provider", id="add-provider", variant="primary")
                    yield Button("Set Primary", id="set-primary")
                    yield Button("Add Fallback", id="add-fallback")
                    yield Button("Test", id="test-provider")
            
            # Channels 标签页
            with TabPane("Channels", id="channels-tab"):
                yield DataTable(id="channels-table", cursor_type="row")
                with Horizontal(classes="button-row"):
                    yield Button("Add Channel", id="add-channel", variant="primary")
                    yield Button("Toggle", id="toggle-channel")
                    yield Button("Remove", id="remove-channel", variant="error")
            
            # Skills 标签页
            with TabPane("Skills", id="skills-tab"):
                yield DataTable(id="skills-table", cursor_type="row")
                with Horizontal(classes="button-row"):
                    yield Button("Install", id="install-skill", variant="primary")
                    yield Button("Update", id="update-skill")
                    yield Button("Remove", id="remove-skill", variant="error")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """挂载时初始化"""
        self.update_status()
        self.load_models()
        self.load_channels()
        self.load_skills()
    
    def update_status(self):
        """更新状态栏"""
        primary = self.manager.get_primary_model()
        fallbacks = self.manager.get_fallbacks()
        providers = self.manager.list_providers()
        
        status_text = f"[bold]Primary:[/bold] {primary}  |  [bold]Providers:[/bold] {len(providers)}  |  [bold]Fallbacks:[/bold] {len(fallbacks)}"
        self.query_one("#status-bar", Static).update(status_text)
    
    def load_models(self):
        """加载 Models 数据"""
        table = self.query_one("#models-table", DataTable)
        table.clear(columns=True)
        
        # 添加列
        table.add_columns("Provider", "Models", "API Key", "Status")
        
        # 添加数据
        for provider in self.manager.list_providers():
            table.add_row(
                provider['name'],
                str(provider['model_count']),
                provider['api_key'],
                "✅"
            )
    
    def load_channels(self):
        """加载 Channels 数据"""
        table = self.query_one("#channels-table", DataTable)
        table.clear(columns=True)
        
        # 添加列
        table.add_columns("Channel", "Type", "Status", "Config")
        
        # 添加数据
        channels = self.manager.list_channels()
        if channels:
            for channel in channels:
                table.add_row(
                    channel['name'],
                    channel['type'],
                    "✅ Enabled" if channel['enabled'] else "❌ Disabled",
                    channel['config']
                )
        else:
            table.add_row("(No channels)", "", "", "")
    
    def load_skills(self):
        """加载 Skills 数据"""
        table = self.query_one("#skills-table", DataTable)
        table.clear(columns=True)
        
        # 添加列
        table.add_columns("Skill", "Version", "Status", "Location")
        
        # 扫描 skills 目录
        import subprocess
        try:
            result = subprocess.run(
                ['clawhub', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.strip() and not line.startswith('─'):
                        parts = line.split()
                        if len(parts) >= 2:
                            table.add_row(parts[0], parts[1], "✅", "ClawHub")
            else:
                table.add_row("(Run 'clawhub list')", "", "", "")
        except:
            table.add_row("(clawhub not available)", "", "", "")
    
    def action_refresh(self):
        """刷新数据"""
        self.update_status()
        self.load_models()
        self.load_channels()
        self.load_skills()
        self.notify("Refreshed")
    
    def action_save(self):
        """保存配置"""
        self.notify("Configuration auto-saved")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        button_id = event.button.id
        
        # Models 操作
        if button_id == "add-provider":
            result = await self.push_screen_wait(AddProviderScreen())
            if result:
                name, url, key = result
                try:
                    self.manager.add_provider(name, url, key)
                    self.load_models()
                    self.update_status()
                    self.notify(f"✅ Provider '{name}' added")
                except Exception as e:
                    self.notify(f"❌ Error: {e}", severity="error")
        
        elif button_id == "set-primary":
            table = self.query_one("#models-table", DataTable)
            if table.cursor_row < len(table.rows):
                provider_name = table.get_row_at(table.cursor_row)[0]
                models = self.manager.list_models(provider_name)
                if models:
                    model_id = models[0]['full_id']
                    self.manager.set_primary_model(model_id)
                    self.update_status()
                    self.notify(f"✅ Primary set to {model_id}")
        
        elif button_id == "add-fallback":
            table = self.query_one("#models-table", DataTable)
            if table.cursor_row < len(table.rows):
                provider_name = table.get_row_at(table.cursor_row)[0]
                models = self.manager.list_models(provider_name)
                if models:
                    model_id = models[0]['full_id']
                    self.manager.add_fallback(model_id)
                    self.update_status()
                    self.notify(f"✅ Added {model_id} to fallbacks")
        
        elif button_id == "test-provider":
            table = self.query_one("#models-table", DataTable)
            if table.cursor_row < len(table.rows):
                provider_name = table.get_row_at(table.cursor_row)[0]
                try:
                    result = self.manager.test_provider(provider_name)
                    if result['success']:
                        self.notify(f"✅ {provider_name} OK")
                    else:
                        self.notify(f"❌ {provider_name} Failed", severity="error")
                except Exception as e:
                    self.notify(f"❌ Error: {e}", severity="error")
        
        # Channels 操作
        elif button_id == "add-channel":
            result = await self.push_screen_wait(AddChannelScreen())
            if result:
                name, channel_type, token = result
                try:
                    self.manager.add_channel(name, channel_type, {'token': token})
                    self.load_channels()
                    self.notify(f"✅ Channel '{name}' added")
                except Exception as e:
                    self.notify(f"❌ Error: {e}", severity="error")
        
        elif button_id == "toggle-channel":
            table = self.query_one("#channels-table", DataTable)
            if table.cursor_row < len(table.rows):
                channel_name = table.get_row_at(table.cursor_row)[0]
                if channel_name != "(No channels)":
                    try:
                        new_state = self.manager.toggle_channel(channel_name)
                        self.load_channels()
                        state_text = "enabled" if new_state else "disabled"
                        self.notify(f"✅ {channel_name} {state_text}")
                    except Exception as e:
                        self.notify(f"❌ Error: {e}", severity="error")
        
        elif button_id == "remove-channel":
            table = self.query_one("#channels-table", DataTable)
            if table.cursor_row < len(table.rows):
                channel_name = table.get_row_at(table.cursor_row)[0]
                if channel_name != "(No channels)":
                    try:
                        self.manager.remove_channel(channel_name)
                        self.load_channels()
                        self.notify(f"✅ Channel '{channel_name}' removed")
                    except Exception as e:
                        self.notify(f"❌ Error: {e}", severity="error")
        
        # Skills 操作
        elif button_id == "install-skill":
            self.notify("Use: clawhub install <skill-name>")
        
        elif button_id == "update-skill":
            self.notify("Use: clawhub update <skill-name>")
        
        elif button_id == "remove-skill":
            self.notify("Use: clawhub remove <skill-name>")


def main():
    app = ClawAPITUI()
    app.run()


if __name__ == "__main__":
    main()
