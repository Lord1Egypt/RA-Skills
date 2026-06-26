#!/usr/bin/env python3
"""
collectors/stealth.py - Playwright反检测模块
提供完整的浏览器指纹隐藏和反检测能力

使用方法：
1. 独立使用（推荐）：
   from collectors.stealth import stealth_context, apply_stealth
   context = browser.new_context()
   apply_stealth(context)  # 注入反检测脚本

2. 与BrowserPlaywright配合：
   from browser.playwright import BrowserPlaywright
   browser = BrowserPlaywright()
   browser.apply_stealth()  # BrowserPlaywright已有内置实现

3. 作为BrowserCollector的插件：
   collector = BrowserCollector()
   collector.apply_stealth()  # 自动注入所有反检测脚本
"""

import random
from typing import Optional, List, Dict, Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


# ==================== 反检测JS脚本库 ====================

STEALTH_SCRIPTS: Dict[str, str] = {}


def _init_stealth_scripts():
    global STEALTH_SCRIPTS

    STEALTH_SCRIPTS = {

        # ---- 基础 ----

        'webdriver_hide': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
            set: undefined,
            configurable: true
        });
        delete window.__webdriver_evaluate;
        delete window.__selenium_evaluate;
        delete window.__webdriver_script_function;
        delete window.__webdriver_script_func;
        delete window.__webdriver_script_executed;
        delete window.__webdriver_evaluate_;
        delete window['__webdriverFunc'];
        delete window.$cdc_;
        delete window.$chrome_;
        ''',

        'chrome_object': '''
        window.chrome = (function() {
            function func() {}
            func.prototype = {
                runtime: {
                    id: '',
                    OnInstalledReason: {},
                    OnStartupReason: {},
                    getPlatformInfo: function() {},
                    getManifest: function() { return {}; },
                    connect: function() { return { onMessage: {}, postMessage: function() {} }; }
                },
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
            return new func();
        })();
        Object.defineProperty(navigator, 'vendor', {
            get: () => 'Google Inc.',
            configurable: true
        });
        ''',

        'plugins': '''
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {
                    name: 'Chrome PDF Plugin',
                    description: 'Portable Document Format',
                    filename: 'internal-pdf-viewer'
                },
                {
                    name: 'Chrome PDF Viewer',
                    description: '',
                    filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'
                },
                {
                    name: 'Native Client',
                    description: '',
                    filename: 'internal-nacl-plugin'
                },
                {
                    name: 'Widevine Content Decryption Module',
                    description: 'Widevine DRM',
                    filename: 'internal-widevinecdm'
                }
            ],
            configurable: true
        });
        Object.defineProperty(navigator, 'mimeTypes', {
            get: () => [
                { type: 'application/pdf', suffixes: 'pdf', description: 'Portable Document Format' },
                { type: 'application/x-nacl', suffixes: 'nexe', description: 'Native Client Executable' },
                { type: 'application/x-pnacl', suffixes: 'pnacl', description: 'Portable Native Client Executable' }
            ],
            configurable: true
        });
        ''',

        'languages': '''
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en-US', 'en', 'ja', 'ko'],
            configurable: true
        });
        ''',

        # ---- 进阶 ----

        'canvas_randomize': '''
        (function() {
            var origGetContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type, attributes) {
                var context = origGetContext.call(this, type, attributes);
                if (type === '2d') {
                    var origFillText = context.fillText;
                    context.fillText = function() {
                        var args = Array.prototype.slice.call(arguments);
                        if (args.length >= 3) {
                            var jitter = (Math.random() - 0.5) * 0.5;
                            args[1] += jitter;
                            args[2] += jitter;
                        }
                        return origFillText.apply(this, args);
                    };
                    var origStrokeText = context.strokeText;
                    context.strokeText = function() {
                        var args = Array.prototype.slice.call(arguments);
                        if (args.length >= 3) {
                            var jitter = (Math.random() - 0.5) * 0.5;
                            args[1] += jitter;
                            args[2] += jitter;
                        }
                        return origStrokeText.apply(this, args);
                    };
                }
                return context;
            };
        })();
        ''',

        'webgl_spoof': '''
        (function() {
            var vendors = ['Google Inc. (Intel)', 'Google Inc. (NVIDIA)', 'Apple Inc.'];
            var renderers = [
                'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)',
                'ANGLE (NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)',
                'Apple M1 Pro'
            ];
            var origGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(param) {
                if (param === 37445) return vendors[Math.floor(Math.random() * vendors.length)];
                if (param === 37446) return renderers[Math.floor(Math.random() * renderers.length)];
                if (param === 37447) return '{\"compilationInfo\":\"WebGL 2.0\"}';
                return origGetParameter.call(this, param);
            };
            var origGetExtension = WebGLRenderingContext.prototype.getExtension;
            WebGLRenderingContext.prototype.getExtension = function(name) {
                if (name === 'WEBGL_debug_renderer_info') return null;
                return origGetExtension.call(this, name);
            };
        })();
        ''',

        'audio_context': '''
        (function() {
            var origCreateDynamicsCompressor = AudioContext.prototype.createDynamicsCompressor;
            AudioContext.prototype.createDynamicsCompressor = function() {
                var node = origCreateDynamicsCompressor.call(this);
                var origGetValue = node.getValue ? node.getValue.bind(node) : null;
                if (origGetValue) {
                    node.getValue = function() {
                        var v = origGetValue();
                        if (typeof v === 'number') {
                            return v + (Math.random() - 0.5) * 1e-10;
                        }
                        return v;
                    };
                }
                return node;
            };
        })();
        ''',

        'permissions_api': '''
        (function() {
            var origQuery = Permissions.prototype.query;
            Permissions.prototype.query = function(permission) {
                return origQuery.call(this, permission).then(function(result) {
                    if (result.state === 'prompt') {
                        Object.defineProperty(result, 'state', {
                            get: function() { return 'granted'; },
                            configurable: true
                        });
                    }
                    return result;
                });
            };
        })();
        ''',

        # ---- 浏览器特征伪装 ----

        'connection_info': '''
        Object.defineProperty(navigator, 'connection', {
            get: () => ({
                effectiveType: '4g',
                downlink: 10,
                rtt: 50,
                downlinkMax: 1000,
                saveData: false
            }),
            configurable: true
        });
        ''',

        'device_memory': '''
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 8,
            configurable: true
        });
        ''',

        'hardware_concurrency': '''
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => 8,
            configurable: true
        });
        ''',

        'platform': '''
        Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32',
            configurable: true
        });
        ''',
    }


_init_stealth_scripts()


# ==================== 主要API ====================

class StealthConfig:
    """
    反检测配置

    Usage:
        config = StealthConfig(
            level='medium',       # basic / medium / aggressive
            randomize=True,      # 是否随机化某些指纹
            exclude=['audio_context']  # 排除的脚本
        )
        apply_stealth(context, config)
    """

    PRESETS = {
        'basic': ['webdriver_hide', 'chrome_object', 'plugins', 'languages'],
        'medium': [
            'webdriver_hide', 'chrome_object', 'plugins', 'languages',
            'canvas_randomize', 'webgl_spoof', 'permissions_api'
        ],
        'aggressive': [
            'webdriver_hide', 'chrome_object', 'plugins', 'languages',
            'canvas_randomize', 'webgl_spoof', 'audio_context',
            'permissions_api', 'connection_info', 'device_memory',
            'hardware_concurrency', 'platform'
        ],
    }

    def __init__(self,
                 level: str = 'medium',
                 randomize: bool = True,
                 exclude: Optional[List[str]] = None,
                 extra_scripts: Optional[Dict[str, str]] = None):
        self.level = level
        self.randomize = randomize
        self.exclude = exclude or []
        self.extra_scripts = extra_scripts or {}

        self._scripts = self.PRESETS.get(level, self.PRESETS['medium']).copy()

        # 合并 extra_scripts
        for name, script in self.extra_scripts.items():
            if name not in self._scripts:
                self._scripts.append(name)
                STEALTH_SCRIPTS[name] = script

        # 应用排除
        self._scripts = [s for s in self._scripts if s not in self.exclude]

    def get_combined_script(self) -> str:
        """获取合并后的反检测脚本（注入到页面）"""
        scripts = [STEALTH_SCRIPTS.get(name, '') for name in self._scripts]
        combined = '\n'.join(scripts)

        if self.randomize:
            combined = self._add_randomization(combined)

        return combined

    def _add_randomization(self, script: str) -> str:
        """在脚本中加入随机性"""
        # 替换固定的vendor/renderer
        import re
        script = re.sub(
            r"vendors\[Math\.floor\(Math\.random\(\) \* vendors\.length\)\]",
            "vendors[Math.floor(Math.random() * vendors.length)]",
            script
        )
        return script


def apply_stealth(context: BrowserContext,
                  config: Optional[StealthConfig] = None,
                  as_init_script: bool = True):
    """
    向 BrowserContext 应用反检测

    Args:
        context: playwright BrowserContext
        config: StealthConfig 配置，默认 basic
        as_init_script: True=add_init_script（推荐），False=evaluate
    """
    if config is None:
        config = StealthConfig(level='medium')

    script = config.get_combined_script()

    if as_init_script:
        # 在页面JS执行前注入（覆盖navigator属性）
        context.add_init_script(script)
    else:
        # 通过 CDP evaluate（不推荐，有些属性在init时已读取）
        context.new_page().evaluate(script)


def stealth_context(browser: Browser,
                     config: Optional[StealthConfig] = None,
                     **context_kwargs) -> BrowserContext:
    """
    创建带反检测的 BrowserContext

    Usage:
        browser = pw.chromium.launch()
        context = stealth_context(browser, level='medium')

    等价于:
        context = browser.new_context(**kwargs)
        apply_stealth(context)
    """
    defaults = {
        'viewport': {'width': 1920, 'height': 1080},
        'locale': 'zh-CN',
        'timezone_id': 'Asia/Shanghai',
        'ignore_https_errors': True,
    }
    defaults.update(context_kwargs)

    context = browser.new_context(**defaults)
    apply_stealth(context, config)
    return context


def stealth_page(page: Page,
                 config: Optional[StealthConfig] = None) -> Page:
    """
    向已有 Page 应用反检测（运行时脚本）

    用于：Page已创建后的额外增强

    注意：最好在Context级别用add_init_script，这里是补充
    """
    if config is None:
        config = StealthConfig(level='medium')
    script = config.get_combined_script()
    page.evaluate(script)
    return page


# ---- CLI ----

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Stealth反检测配置工具')
    parser.add_argument('--level', choices=['basic', 'medium', 'aggressive'],
                        default='medium', help='反检测级别')
    parser.add_argument('--list', action='store_true', help='列出所有可用脚本')
    args = parser.parse_args()

    if args.list:
        print("Available stealth scripts:")
        for name in STEALTH_SCRIPTS:
            desc = name.replace('_', ' ').title()
            in_basic = 'basic' if name in StealthConfig.PRESETS['basic'] else ''
            in_medium = 'medium' if name in StealthConfig.PRESETS['medium'] else ''
            in_aggressive = 'aggressive' if name in StealthConfig.PRESETS['aggressive'] else ''
            print(f"  {name:25s} [{in_basic:8s} {in_medium:8s} {in_aggressive:11s}]")
        return 0

    config = StealthConfig(level=args.level)
    script = config.get_combined_script()
    print(f"Combined script ({len(script)} chars):")
    print(script[:500] + "..." if len(script) > 500 else script)


if __name__ == '__main__':
    import sys
    sys.exit(main())
