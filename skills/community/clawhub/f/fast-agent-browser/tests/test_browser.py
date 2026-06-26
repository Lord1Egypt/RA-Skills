"""
Test suite for Agent Browser
"""

import pytest
from src.browser import BrowserAgent


class TestBrowserAgent:
    """Test BrowserAgent class"""
    
    def test_init(self):
        """Test browser agent initialization"""
        agent = BrowserAgent(headless=True)
        assert agent.headless == True
        assert agent.playwright is None
        assert agent.browser is None
        assert agent.page is None
    
    def test_context_manager(self):
        """Test context manager"""
        with BrowserAgent() as agent:
            assert agent.playwright is not None
            assert agent.browser is not None
            assert agent.page is not None
        
        # After context, should be closed
        assert agent.playwright is None
        assert agent.browser is None
        assert agent.page is None
    
    def test_open_url(self):
        """Test opening URL"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            assert "example.com" in agent.page.url
    
    def test_get_title(self):
        """Test getting page title"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            # Example.com has title "Example Domain"
            assert agent.page.title() == "Example Domain"
    
    def test_get_url(self):
        """Test getting current URL"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            assert agent.page.url == "https://example.com/"
    
    def test_screenshot(self, tmp_path):
        """Test taking screenshot"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            screenshot_path = tmp_path / "test.png"
            agent.screenshot(str(screenshot_path))
            assert screenshot_path.exists()
            assert screenshot_path.stat().st_size > 0
    
    def test_get_text(self):
        """Test getting text content"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            text = agent.get_text("h1")
            assert "Example" in text
    
    def test_get_html(self):
        """Test getting HTML"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            html = agent.get_html("body")
            assert "<body" in html or "body" in html.lower()
    
    def test_is_visible(self):
        """Test checking visibility"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            # h1 should be visible
            assert agent.is_visible("h1") == True
            # Non-existent element should return False
            assert agent.is_visible("#nonexistent") == False
    
    def test_snapshot(self):
        """Test getting accessibility snapshot"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            tree = agent.snapshot()
            assert tree is not None
            assert isinstance(tree, str)
    
    def test_snapshot_interactive(self):
        """Test getting interactive elements only"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            tree = agent.snapshot(interactive=True)
            # Should filter to interactive elements only
            assert tree is not None
    
    def test_snapshot_compact(self):
        """Test getting compact snapshot"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            tree = agent.snapshot(compact=True)
            assert tree is not None
    
    def test_snapshot_depth(self):
        """Test limiting snapshot depth"""
        with BrowserAgent() as agent:
            agent.open("https://example.com")
            tree = agent.snapshot(depth=2)
            assert tree is not None


class TestCLI:
    """Test CLI commands"""
    
    def test_cli_help(self):
        """Test CLI help"""
        from click.testing import CliRunner
        from agent_browser import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Commands' in result.output
    
    def test_cli_open(self):
        """Test open command"""
        from click.testing import CliRunner
        from agent_browser import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['open', 'https://example.com'])
        assert result.exit_code == 0
        assert 'Opened' in result.output
    
    def test_cli_snapshot(self):
        """Test snapshot command"""
        from click.testing import CliRunner
        from agent_browser import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['snapshot'])
        assert result.exit_code == 0
    
    def test_cli_close(self):
        """Test close command"""
        from click.testing import CliRunner
        from agent_browser import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['close'])
        assert result.exit_code == 0
        assert 'closed' in result.output.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
