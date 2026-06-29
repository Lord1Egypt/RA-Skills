#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color Toolkit - HTML预览生成器
生成专业的颜色预览HTML页面
"""

import os
from typing import List, Dict, Any, Optional
from color_toolkit import ColorCore, convert_color, get_contrast, get_palette, get_complementary


def generate_color_swatch_html(hex_color: str, size: int = 150) -> str:
    """生成单个颜色色块HTML"""
    rgb = ColorCore.hex_to_rgb(hex_color)
    luminance = float(ColorCore.calculate_luminance(rgb.r, rgb.g, rgb.b))
    text_color = "#FFFFFF" if luminance < 0.5 else "#000000"

    hsl = ColorCore.rgb_to_hsl(rgb.r, rgb.g, rgb.b)

    return f'''
    <div class="color-swatch" style="background-color: {hex_color}; width: {size}px; height: {size}px;">
        <div class="swatch-info" style="color: {text_color};">
            <div class="hex">{hex_color.upper()}</div>
            <div class="rgb">RGB({rgb.r}, {rgb.g}, {rgb.b})</div>
        </div>
    </div>
    '''


def generate_contrast_preview_html(color1: str, color2: str) -> str:
    """生成两种颜色的对比度预览HTML"""
    contrast_data = get_contrast(color1, color2, "all")
    rgb1 = ColorCore.hex_to_rgb(color1)
    rgb2 = ColorCore.hex_to_rgb(color2)

    # 判断文字颜色
    text_on_c1 = "#FFFFFF" if float(ColorCore.calculate_luminance(rgb1.r, rgb1.g, rgb1.b)) < 0.5 else "#000000"
    text_on_c2 = "#FFFFFF" if float(ColorCore.calculate_luminance(rgb2.r, rgb2.g, rgb2.b)) < 0.5 else "#000000"

    wcag_pass = contrast_data["wcag2"]["pass"]
    apca_pass = contrast_data["apca"]["pass"]

    return f'''
    <div class="contrast-preview">
        <h3>对比度测试</h3>
        <div class="contrast-grid">
            <!-- 背景色1 + 文字色2 -->
            <div class="contrast-box" style="background-color: {color1}; color: {color2};">
                <div class="box-label">背景: {color1.upper()}</div>
                <div class="box-text">前景: {color2.upper()}</div>
                <div class="box-sample">Aa 颜色预览</div>
            </div>
            <!-- 背景色2 + 文字色1 -->
            <div class="contrast-box" style="background-color: {color2}; color: {color1};">
                <div class="box-label">背景: {color2.upper()}</div>
                <div class="box-text">前景: {color1.upper()}</div>
                <div class="box-sample">Aa 颜色预览</div>
            </div>
            <!-- 大文本 -->
            <div class="contrast-box large-text" style="background-color: {color1}; color: {color2};">
                <div class="box-sample" style="font-size: 24px;">大号文本 (24px+)</div>
                <div class="box-sample" style="font-size: 18px;">标准文本 (18px)</div>
            </div>
        </div>

        <div class="contrast-results">
            <h4>对比度评估结果</h4>
            <table class="contrast-table">
                <thead>
                    <tr>
                        <th>算法</th>
                        <th>数值</th>
                        <th>等级</th>
                        <th>无障碍</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>WCAG 2.1</td>
                        <td class="value">{contrast_data["wcag2"]["value"]}</td>
                        <td><span class="badge" style="background-color: {contrast_data["wcag2"]["color"]}">{contrast_data["wcag2"]["level"]}</span></td>
                        <td>{'✅ 通过' if wcag_pass else '❌ 未通过'}</td>
                    </tr>
                    <tr>
                        <td>APCA</td>
                        <td class="value">{contrast_data["apca"]["value"]} Lc</td>
                        <td><span class="badge" style="background-color: {contrast_data["apca"]["color"]}">{contrast_data["apca"]["level"]}</span></td>
                        <td>{'✅ 通过' if apca_pass else '❌ 未通过'}</td>
                    </tr>
                    <tr>
                        <td>CIELAB ΔE*ab</td>
                        <td class="value">{contrast_data["cielab"]["value"]}</td>
                        <td><span class="badge" style="background-color: {contrast_data["cielab"]["color"]}">{contrast_data["cielab"]["level"]}</span></td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td>CIEDE2000</td>
                        <td class="value">{contrast_data["ciede2000"]["value"]}</td>
                        <td><span class="badge" style="background-color: {contrast_data["ciede2000"]["color"]}">{contrast_data["ciede2000"]["level"]}</span></td>
                        <td>-</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    '''


def generate_palette_preview_html(colors: List[str], palette_name: str = "配色方案") -> str:
    """生成调色板预览HTML"""
    swatches_html = ""
    for color in colors:
        swatches_html += generate_color_swatch_html(color, 120)

    return f'''
    <div class="palette-preview">
        <h3>{palette_name}</h3>
        <div class="swatches-row">
            {swatches_html}
        </div>
    </div>
    '''


def generate_gradient_preview_html(colors: List[str]) -> str:
    """生成渐变预览HTML"""
    if len(colors) < 2:
        return ""

    # 线性渐变
    linear_gradient = "linear-gradient(to right, " + ", ".join(colors) + ")"
    # 径向渐变
    radial_gradient = "radial-gradient(circle, " + ", ".join(colors) + ")"

    return f'''
    <div class="gradient-preview">
        <h3>渐变效果</h3>
        <div class="gradient-box" style="background: {linear_gradient}; height: 80px; border-radius: 8px; margin-bottom: 16px;">
            <span style="color: white; text-shadow: 0 1px 3px rgba(0,0,0,0.5); padding: 8px; display: flex; align-items: center; height: 100%;">线性渐变 (Linear)</span>
        </div>
        <div class="gradient-box" style="background: {radial_gradient}; height: 80px; border-radius: 8px;">
            <span style="color: white; text-shadow: 0 1px 3px rgba(0,0,0,0.5); padding: 8px; display: flex; align-items: center; height: 100%;">径向渐变 (Radial)</span>
        </div>
    </div>
    '''


def generate_full_preview_html(color_input: str,
                                title: str = "颜色预览",
                                show_complementary: bool = True,
                                show_contrast: bool = True,
                                output_path: Optional[str] = None) -> str:
    """
    生成完整的颜色预览HTML页面

    Args:
        color_input: 颜色输入（HEX/RGB/HSL格式）
        title: 页面标题
        show_complementary: 是否显示互补色
        show_contrast: 是否显示对比度测试
        output_path: 输出文件路径（可选）

    Returns:
        生成的HTML内容
    """
    # 解析颜色
    color_info = convert_color(color_input)
    hex_color = color_info["hex"]
    rgb = color_info["rgb"]
    hsl = color_info["hsl"]
    luminance = float(color_info["luminance"])

    # 获取互补色
    comp_data = get_complementary(color_input)
    comp_hex = comp_data["complementary"]

    # 获取调色板
    triadic_palette = get_palette(color_input, "triadic")
    analogous_palette = get_palette(color_input, "analogous")

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {hex_color}</title>
    <style>
        :root {{
            --primary: {hex_color};
            --complementary: {comp_hex};
            --text-dark: #1a1a1a;
            --text-light: #ffffff;
            --bg-light: #f8f9fa;
            --bg-dark: #2d3436;
            --border: #dee2e6;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, {hex_color} 0%, {comp_hex} 100%);
            padding: 40px;
            text-align: center;
            color: white;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}

        .content {{
            padding: 30px;
        }}

        h2 {{
            color: var(--text-dark);
            margin: 30px 0 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--primary);
            font-size: 1.5rem;
        }}

        h3 {{
            color: var(--text-dark);
            margin: 20px 0 15px;
            font-size: 1.2rem;
        }}

        /* 主色展示 */
        .main-color-display {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }}

        .main-swatch {{
            flex: 1;
            height: 150px;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: {"white" if float(color_info["luminance"]) < 0.5 else "black"};
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}

        .main-swatch.primary {{
            background-color: {hex_color};
        }}

        .main-swatch.complementary {{
            background-color: {comp_hex};
        }}

        .swatch-label {{
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 5px;
        }}

        .swatch-hex {{
            font-size: 1.5rem;
            font-weight: bold;
        }}

        /* 颜色编码表格 */
        .color-values {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .value-card {{
            background: var(--bg-light);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid var(--primary);
        }}

        .value-card .label {{
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 5px;
        }}

        .value-card .value {{
            font-size: 1.1rem;
            font-weight: 600;
            font-family: "SF Mono", Monaco, monospace;
        }}

        /* 色块 */
        .color-swatch {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .swatch-info {{
            text-align: center;
            padding: 10px;
        }}

        .swatch-info .hex {{
            font-weight: bold;
            font-size: 1rem;
        }}

        .swatch-info .rgb {{
            font-size: 0.75rem;
            opacity: 0.8;
        }}

        /* 调色板 */
        .swatches-row {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }}

        /* 对比度测试 */
        .contrast-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .contrast-box {{
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}

        .contrast-box .box-label {{
            font-size: 0.8rem;
            opacity: 0.7;
            margin-bottom: 5px;
        }}

        .contrast-box .box-sample {{
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 10px;
        }}

        /* 对比度表格 */
        .contrast-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        .contrast-table th,
        .contrast-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}

        .contrast-table th {{
            background: var(--bg-light);
            font-weight: 600;
        }}

        .contrast-table .value {{
            font-family: "SF Mono", Monaco, monospace;
            font-weight: bold;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            color: white;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        /* 渐变 */
        .gradient-preview {{
            margin: 20px 0;
        }}

        /* UI组件预览 */
        .ui-preview {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin: 20px 0;
        }}

        .ui-button {{
            display: inline-block;
            padding: 12px 24px;
            background: var(--primary);
            color: {"white" if float(color_info["luminance"]) < 0.5 else "black"};
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .ui-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        .ui-button.outline {{
            background: transparent;
            border: 2px solid var(--primary);
            color: var(--primary);
        }}

        .ui-button.complement {{
            background: var(--complementary);
            color: {{"white" if luminance < 0.5 else "black"}};
        }}

        .ui-card {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}

        .ui-card-header {{
            background: var(--primary);
            color: {"white" if float(color_info["luminance"]) < 0.5 else "black"};
            padding: 15px;
            margin: -20px -20px 20px -20px;
            border-radius: 10px 10px 0 0;
        }}

        /* 响应式 */
        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            .main-color-display {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="subtitle">{color_info["name"]} - {color_info["temperature"]} / {color_info["family"]}</div>
        </div>

        <div class="content">
            <!-- 颜色信息 -->
            <h2>🎨 颜色信息</h2>

            <div class="main-color-display">
                <div class="main-swatch primary">
                    <div class="swatch-label">主色</div>
                    <div class="swatch-hex">{hex_color.upper()}</div>
                </div>
                <div class="main-swatch complementary">
                    <div class="swatch-label">互补色</div>
                    <div class="swatch-hex">{comp_hex.upper()}</div>
                </div>
            </div>

            <div class="color-values">
                <div class="value-card">
                    <div class="label">HEX</div>
                    <div class="value">{hex_color.upper()}</div>
                </div>
                <div class="value-card">
                    <div class="label">RGB</div>
                    <div class="value">rgb({rgb['r']}, {rgb['g']}, {rgb['b']})</div>
                </div>
                <div class="value-card">
                    <div class="label">HSL</div>
                    <div class="value">hsl({hsl['h']}, {hsl['s']}%, {hsl['l']}%)</div>
                </div>
                <div class="value-card">
                    <div class="label">HSV</div>
                    <div class="value">hsv({color_info['hsv']['h']}, {color_info['hsv']['s']}%, {color_info['hsv']['v']}%)</div>
                </div>
                <div class="value-card">
                    <div class="label">CMYK</div>
                    <div class="value">cmyk({color_info['cmyk']['c']}%, {color_info['cmyk']['m']}%, {color_info['cmyk']['y']}%, {color_info['cmyk']['k']}%)</div>
                </div>
                <div class="value-card">
                    <div class="label">亮度</div>
                    <div class="value">{color_info['luminance']}</div>
                </div>
                <div class="value-card">
                    <div class="label">灰度</div>
                    <div class="value">Gray({color_info['grayscale']})</div>
                </div>
                <div class="value-card">
                    <div class="label">色系</div>
                    <div class="value">{color_info['family']}</div>
                </div>
            </div>

            <!-- 调色板 -->
            <h2>🎭 配色方案</h2>

            <h3>三色组 (Triadic)</h3>
            {generate_palette_preview_html(triadic_palette['colors'], '三色组')}

            <h3>类似色 (Analogous)</h3>
            {generate_palette_preview_html(analogous_palette['colors'], '类似色')}

            <h3>渐变效果</h3>
            {generate_gradient_preview_html(triadic_palette['colors'])}

            <!-- 对比度测试 -->
            <h2>♿ 无障碍对比</h2>
            {generate_contrast_preview_html(hex_color, comp_hex)}
            {generate_contrast_preview_html(hex_color, '#FFFFFF')}
            {generate_contrast_preview_html(hex_color, '#000000')}

            <!-- UI组件预览 -->
            <h2>🧩 UI组件预览</h2>
            <div class="ui-preview">
                <div class="ui-card">
                    <div class="ui-card-header">卡片标题</div>
                    <p>这是一个使用主色作为标题背景的卡片组件示例，展示颜色在实际UI中的应用效果。</p>
                </div>

                <div>
                    <button class="ui-button">主要按钮</button>
                    <button class="ui-button outline">描边按钮</button>
                    <button class="ui-button complement">强调按钮</button>
                </div>
            </div>

            <div style="text-align: center; padding: 20px; color: #666; font-size: 0.9rem;">
                由 Color Toolkit 自动生成 | {hex_color.upper()}
            </div>
        </div>
    </div>
</body>
</html>'''

    # 保存文件
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path

    return html


def generate_palette_page_html(colors: List[str],
                                palette_title: str = "配色方案",
                                output_path: Optional[str] = None) -> str:
    """生成完整调色板预览页面"""

    # 生成各颜色的详细信息
    color_details = []
    for color in colors:
        info = convert_color(color)
        color_details.append(info)

    # 生成色块HTML
    swatches_html = ""
    for detail in color_details:
        rgb = detail["rgb"]
        hex_val = detail["hex"]
        text_color = "#FFFFFF" if float(detail["luminance"]) < 0.5 else "#000000"

        swatches_html += f'''
        <div class="color-item">
            <div class="color-preview" style="background-color: {hex_val}; color: {text_color};">
                <div class="hex-label">{hex_val.upper()}</div>
            </div>
            <div class="color-details">
                <div class="detail-row"><span class="detail-label">RGB</span><span class="detail-value">rgb({rgb['r']}, {rgb['g']}, {rgb['b']})</span></div>
                <div class="detail-row"><span class="detail-label">HSL</span><span class="detail-value">hsl({detail['hsl']['h']}, {detail['hsl']['s']}%, {detail['hsl']['l']}%)</span></div>
                <div class="detail-row"><span class="detail-label">CMYK</span><span class="detail-value">cmyk({detail['cmyk']['c']}%, {detail['cmyk']['m']}%, {detail['cmyk']['y']}%, {detail['cmyk']['k']}%)</span></div>
                <div class="detail-row"><span class="detail-label">亮度</span><span class="detail-value">{detail['luminance']}</span></div>
            </div>
        </div>
        '''

    # 生成渐变预览
    gradient_linear = "linear-gradient(135deg, " + ", ".join(colors) + ")"
    gradient_linear_reverse = "linear-gradient(135deg, " + ", ".join(reversed(colors)) + ")"
    gradient_radial = "radial-gradient(circle, " + ", ".join(colors) + ")"

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{palette_title}</title>
    <style>
        :root {{
            --primary: {colors[0] if colors else '#3498db'};
            --bg: #f5f7fa;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            padding: 30px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}

        h1 {{
            text-align: center;
            color: #1a1a1a;
            margin-bottom: 10px;
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }}

        section {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}

        h2 {{
            color: #1a1a1a;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--primary);
        }}

        .color-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}

        .color-item {{
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .color-preview {{
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .hex-label {{
            font-size: 1.2rem;
            font-weight: bold;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }}

        .color-details {{
            background: white;
            padding: 15px;
        }}

        .detail-row {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            font-size: 0.85rem;
        }}

        .detail-label {{
            color: #888;
        }}

        .detail-value {{
            font-family: monospace;
            color: #333;
        }}

        .gradient-showcase {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .gradient-box {{
            height: 60px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 500;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}

        .gradient-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{palette_title}</h1>
        <p class="subtitle">Color Toolkit 自动生成</p>

        <section>
            <h2>🎨 颜色色板</h2>
            <div class="color-grid">
                {swatches_html}
            </div>
        </section>

        <section>
            <h2>🌈 渐变效果</h2>
            <div class="gradient-row">
                <div class="gradient-box" style="background: {gradient_linear};">
                    135° 线性渐变
                </div>
                <div class="gradient-box" style="background: {gradient_linear_reverse};">
                    反向渐变
                </div>
                <div class="gradient-box" style="background: {gradient_radial};">
                    径向渐变
                </div>
            </div>
        </section>

        <section>
            <h2>📋 颜色代码</h2>
            <pre style="background: #1a1a1a; color: #a9dc76; padding: 20px; border-radius: 8px; overflow-x: auto; font-family: monospace;">{chr(10).join([f'{i+1}. {c.upper()}' for i, c in enumerate(colors)])}</pre>
        </section>
    </div>
</body>
</html>'''

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path

    return html


if __name__ == "__main__":
    # 测试
    output = generate_full_preview_html("#3498db", "测试颜色", output_path="test_preview.html")
    print(f"预览文件已生成: {output}")
