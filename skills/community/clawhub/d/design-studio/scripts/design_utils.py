"""Утилиты для дизайн-студии — общие функции для всех скриптов."""

from PIL import Image, ImageDraw, ImageFont
import subprocess
import os

SVG_ICONS_DIR = os.path.join(os.path.dirname(__file__), '..', 'references', 'svg_elements', 'icons')

def find_font(name, size, bold=False):
    """Найти шрифт через fc-match."""
    style = f"{name}:Bold" if bold else name
    try:
        result = subprocess.run(
            ['fc-match', '--format=%{file}', style],
            capture_output=True, text=True, timeout=5
        )
        path = result.stdout.strip()
        if path and os.path.exists(path):
            return ImageFont.truetype(path, size)
    except:
        pass
    return ImageFont.load_default()

def render_svg_icon(svg_path, size=64, color=(255, 255, 255)):
    """Рендерит SVG-иконку в Pillow Image с заданным цветом."""
    try:
        import cairosvg
        from io import BytesIO
        
        # Читаем SVG и меняем цвет
        with open(svg_path, 'r') as f:
            svg_data = f.read()
        
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        svg_data = svg_data.replace('#FFFFFF', hex_color).replace('#ffffff', hex_color)
        svg_data = svg_data.replace('fill="white"', f'fill="{hex_color}"')
        
        png_data = cairosvg.svg2png(bytestring=svg_data.encode(), output_width=size, output_height=size)
        return Image.open(BytesIO(png_data)).convert('RGBA')
    except Exception as e:
        # Fallback: нарисовать кружок
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, size-4, size-4], fill=color + (200,))
        return img

def get_icon(name, size=64, color=(255, 255, 255)):
    """Получить иконку по имени из SVG-библиотеки."""
    svg_path = os.path.join(SVG_ICONS_DIR, f'{name}.svg')
    if os.path.exists(svg_path):
        return render_svg_icon(svg_path, size, color)
    # Fallback
    return render_svg_icon(os.path.join(SVG_ICONS_DIR, 'star.svg'), size, color)

def auto_fit_text(draw, text, font_name, max_width, max_size, min_size=16, bold=False):
    """Подбирает размер шрифта чтобы текст влез в max_width."""
    size = max_size
    while size >= min_size:
        font = find_font(font_name, size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            return font, size
        size -= 4
    return find_font(font_name, min_size, bold), min_size

# Маппинг emoji → SVG иконки
EMOJI_TO_ICON = {
    '📊': 'chart_up', '✅': 'checkmark', '🔍': 'star',
    '⚡': 'lightning', '💰': 'dollar', '🛡': 'shield',
    '⏱': 'clock', '🔧': 'gear', '→': 'arrow_right',
    '📈': 'chart_up', '💡': 'lightning', '⭐': 'star',
    '🎯': 'star', '🔥': 'lightning', '✓': 'checkmark',
}

def replace_emoji_with_icon(text):
    """Убирает emoji из текста, возвращает (чистый_текст, список_иконок)."""
    icons = []
    clean = text
    for emoji, icon_name in EMOJI_TO_ICON.items():
        if emoji in clean:
            icons.append(icon_name)
            clean = clean.replace(emoji, '').strip()
    return clean, icons
