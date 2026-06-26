#!/usr/bin/env python3
"""
PPTX translate script — translates English text in PPTX to target language while preserving template.
Usage: python3 pptx_translate.py <input.pptx> [--output <output.pptx>] [--src-lang en] [--tgt-lang zh]
"""

import argparse
import os
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Register namespaces to preserve them
ET.register_namespace('', 'http://schemas.openxmlformats.org/presentationml/2006/main')
ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
ET.register_namespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')
ET.register_namespace('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006')
ET.register_namespace('c', 'http://schemas.openxmlformats.org/drawingml/2006/chart')
ET.register_namespace('dgm', 'http://schemas.openxmlformats.org/drawingml/2006/diagram')
ET.register_namespace('pic', 'http://schemas.openxmlformats.org/drawingml/2006/picture')
ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
ET.register_namespace('w14', 'http://schemas.microsoft.com/office/word/2010/wordml')
ET.register_namespace('w15', 'http://schemas.microsoft.com/office/word/2010/wordml')
ET.register_namespace('wps', 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape')
ET.register_namespace('wpg', 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup')
ET.register_namespace('wpc', 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas')


def load_translations(src_lang='en', tgt_lang='zh'):
    """Load translation mapping table. Extend this as needed."""
    if src_lang == 'en' and tgt_lang == 'zh':
        return [
            # Slide 1
            ("Customer presentation", "客户演示文稿"),
            ("Meet the new Sonicision", "认识全新 Sonicision"),
            ("The freedom", "自由"),
            ("do more", "多做"),
            ("curved jaw cordless ultrasonic dissection system", "弯曲刀头 Cordless 超声解剖系统"),
            # Slide 2
            ("Table of contents", "目录"),
            ("Introduction", "简介"),
            ("Features and benefits", "产品特点与优势"),
            ("Technology enhancements", "技术增强"),
            ("A design for the whole team", "面向整个团队的设计"),
            ("Competitive comparison", "竞争对比"),
            ("Q & A", "问答"),
            # Slide 3
            ("Still innovating, a decade later", "十年创新，初心不改"),
            ("The future never stops revolutionizing — and neither do we.", "未来持续革新，我们亦是如此。"),
            ("Building on our 10-year history of innovation, our new and expanded Sonicision", "基于10年创新积淀，我们全新升级的 Sonicision"),
            ("7 curved jaw ultrasonic device is here.", "7 弯曲刀头超声设备现已面世。"),
            ("Still the first and only cordless ultrasonic dissector,", "仍是首款且唯一的 Cordless 超声解剖器，"),
            ("7 curved jaw device lets you do more", "7 弯曲刀头设备让您使用一台设备即可完成更多操作"),
            ("with one device.", ""),
            ("curved jaw cordless ultrasonic dissector uses a three-phased algorithm for improved coagulation and hemostatic dissection of vasculature up to and including 7 mm in diameter.", "弯曲刀头 Cordless 超声解剖器采用三相算法，提升凝血和血管止血分离效果，适用于最大 7 mm 直径的血管。"),
            ("Our latest advancement in ultrasonic dissection delivers the economic value", "我们在超声解剖领域的最新突破，为您带来经济价值"),
            ("and safer OR experience", "以及更安全的手术室体验"),
            ("your healthcare setting counts on combined with the cordless freedom", "您的医疗机构所信赖的这一切，结合您所依赖的 Cordless 自由"),
            ("Experience a new level", "体验全新级别的"),
            ("of versatility", "多用性"),
            ("for improved surgical efficiency", "实现更高的手术效率"),
            # Slide 6
            ("One-of-a-kind freedom", "独特的自由"),
            ("Precise access", "精准入路"),
            ("Enhanced versatility", "增强的多用性"),
            ("Improved efficiency", "提升效率"),
            ("in the OR", "在手术室中"),
            ("Freedom", "自由"),
            ("Remains the first and only cordless ultrasonic dissector", "仍是首款且唯一的 Cordless 超声解剖器"),
            ("Is easier to pass during surgical procedures", "在手术过程中更易于传递"),
            ("Enables comfortable use throughout procedures", "使整个手术过程中使用更舒适"),
            ("Improves freedom of movement and mobility", "改善移动和灵活性自由"),
            ("Provides a portable system that enables use in any OR", "提供便携式系统，可在任何手术室中使用"),
            # Slide 7
            ("Precision", "精准"),
            ("Provides precise energy dissection", "提供精准的能量解剖"),
            ("Provides proper access to critical structures in tight spaces", "在狭窄空间中提供对关键结构的适当入路"),
            ("Enables proper visualization of target structures during procedures", "使手术过程中目标结构的可视化更清晰"),
            ("Allows for precise access to tissue planes", "可精准进入组织层面"),
            ("Allows surgeons to hug (or follow) curved anatomical structures", "使外科医生能够紧贴（跟随）弯曲的解剖结构"),
            # Slide 8
            ("Versatility", "多用性"),
            ("Coagulates vessels up to and including 7 mm in diameter in minimum mode and coagulates vessels up to and including 5 mm in diameter in maximum mode", "最小模式下可凝闭最大 7 mm 直径的血管，最大模式下可凝闭最大 5 mm 直径的血管"),
            ("Allows for simple transition between minimum and maximum energy modes without taking the surgeon's eyes off the surgical field", "使医生无需将视线离开手术区域，即可轻松切换最小和最大能量模式"),
            ("Comes in four shaft lengths for use across a wide range of procedures including general, bariatric, colorectal, plastic, urology, GYN, and ENT", "提供四种轴长，适用于包括普通外科、减重外科、结直肠外科、整形外科、泌尿科、妇科和耳鼻喉科在内的广泛手术"),
            ("Offers improved confidence", "提升医生信心"),
            ("and surgical efficiency", "和手术效率"),
            ("over devices that coagulate vessels up to 5 mm", "优于仅能凝闭 5 mm 血管的设备"),
            ("Reduces the need for additional instruments (ties or clips)", "减少对额外器械（结扎线或止血夹）的需求"),
            # Slide 9
            ("Next-generation design meets everyday convenience", "下一代设计，契合日常便捷"),
            ("The reusable generator is a small but mighty powerhouse that:", "可重复使用发生器虽小巧却功能强大："),
            ("Streamlines cleaning and sterilization because it's", "简化清洁和灭菌流程，因为它"),
            ("autowashable", "可自动清洗"),
            ("and autoclavable", "且可高压灭菌"),
            ("Fits in the palm of your hand", "可握于掌心"),
            ("Works for 150 procedures before you need to replace it", "可支持 150 次手术无需更换"),
            # Slide 10
            ("The intuitive, easy-to-use", "直观、易于使用"),
            ("battery charger:", "电池充电器："),
            ("Makes it easy to interpret battery charge status", "使电池充电状态一目了然"),
            ("and battery end-of-life indications", "和电池寿命终止提示"),
            ("Enables efficient battery usage management", "实现高效的电池使用管理"),
            ("The reusable nonsterile battery pack offers:", "可重复使用非无菌电池包特性："),
            ("88% more battery capacity", "电池容量增加 88%"),
            ("Twice the number of procedural uses —", "手术使用次数翻倍 —"),
            ("from 100 to 200", "从 100 次到 200 次"),
            ("Rest assured that batteries will be optimally maintained through", "放心使用，电池在整个使用周期内将得到最佳维护"),
            ("200 procedural uses to deliver reliable power and performance.", "200 次手术使用期间提供可靠的动力和性能。"),
            # Slide 11
            ("Cordless design/ergonomics", "Cordless 设计/人体工学"),
            ("7 curved jaw device contributes to a safer OR.", "7 弯曲刀头设备的 Cordless 设计有助于打造更安全的手术室。"),
            ("curved jaw device improves freedom of movement and mobility.", "弯曲刀头设备的 Cordless 设计改善了移动和灵活性自由。"),
            ("curved jaw device makes it easier to pass the device within surgical procedures.", "弯曲刀头设备的 Cordless 设计使在手术过程中传递设备更加便捷。"),
            ("The self-contained system improves the use of OR space and enables space savings.", "自成一体的系统改善了手术室空间利用，节省空间。"),
            # Slide 12
            ("Setup simplicity", "安装简便"),
            ("7 curved jaw cordless ultrasonic dissector simplifies device setup.", "7 弯曲刀头 Cordless 超声解剖器的集成扭矩扳手设计简化了设备安装。"),
            ("Ease of assembly", "装配便捷"),
            ("allows nurses to have the device ready before the surgeon and patient are in the OR.", "使护士能够在外科医生和患者进入手术室前准备好设备。"),
            ("The troubleshooting steps associated with the device are clear and easy to follow.", "设备相关的故障排除步骤清晰易懂。"),
            ("device is easier to assemble than the Harmonic", "设备比 Harmonic"),
            ("scalpel.", "超声刀更容易组装。"),
            # Slide 13
            ("Battery and charger user interface", "电池和充电器用户界面"),
            ("battery charger is intuitive and easy to use.", "电池充电器直观且易于使用。"),
            ("The battery charge status", "电池充电状态"),
            ("and end-of-life indications", "和电池寿命终止提示"),
            ("are easy to interpret on the", "在"),
            ("battery charger.", "电池充电器上易于读取。"),
            ("battery charger enable efficient battery usage management.", "电池充电器上的电池充电状态和电池寿命终止提示可实现高效的电池使用管理。"),
            # Slide 14
            ("Click for infographic", "点击查看信息图"),
            # Slide 16
            ("References", "参考资料"),
            # Survey footers
            ("surgeons surveyed after use agreed.", "受访外科医生中，使用后表示认同的。"),
            ("nurses surveyed after use agreed.", "受访护士中，使用后表示认同的。"),
            ("nurses surveyed after use answered extremely easy (59%) or easy (24%).", "受访护士中，使用后表示非常容易（59%）或容易（24%）。"),
            ("nurses surveyed after use answered a lot easier (41%) or easier (24%).", "受访护士中，使用后表示轻松很多（41%）或轻松一些（24%）。"),
            # Trademark footer
            ("Medtronic, Medtronic logo, and Engineering the extraordinary are trademarks of Medtronic. ™* Third-party brands are trademarks of their respective owners. All other brands are trademarks of a Medtronic company.", "Medtronic、Medtronic 标志及 Engineering the extraordinary 为 Medtronic 的商标。™* 第三方品牌为其各自所有者的商标。所有其他品牌均为 Medtronic 公司的商标。"),
            # Product components
            ("Product components overview", "产品组件概览"),
            ("New components —", "全新组件 —"),
            ("7 system only", "7 系统专用"),
            ("Shared system components —", "共用系统组件 —"),
            ("7 and Sonicision", "7 与 Sonicision"),
            ("curved jaw systems", "弯曲刀头系统共用"),
            ("Product code", "产品代码"),
            ("Description", "描述"),
            ("7 curved jaw ultrasonic dissector — 13 cm", "7 弯曲刀头超声解剖器 — 13 cm"),
            ("7 curved jaw ultrasonic dissector — 26 cm", "7 弯曲刀头超声解剖器 — 26 cm"),
            ("7 curved jaw ultrasonic dissector — 39 cm", "7 弯曲刀头超声解剖器 — 39 cm"),
            ("7 curved jaw ultrasonic dissector — 48 cm", "7 弯曲刀头超声解剖器 — 48 cm"),
            ("7 reusable generator — A", "7 可重复使用发生器 — A"),
            ("battery charger", "电池充电器"),
            ("reusable battery pack", "可重复使用电池包"),
            ("reusable battery insertion guide", "可重复使用电池插入引导器"),
            ("reusable sterilization tray", "可重复使用灭菌托盘"),
            ("only available in certain countries", "仅在某些国家/地区提供"),
            # Indications
            ("510(k) Indications for Use Statement", "510(k) 适应症声明"),
            ("7 curved jaw cordless ultrasonic dissection device is indicated for soft tissue incisions when bleeding control and minimal thermal injury are desired.", "7 弯曲刀头 Cordless 超声解剖设备适用于需要在控制出血和最小热损伤条件下进行软组织切开的手术。"),
            ("The device can be used as an adjunct to or substitute for electrosurgery, lasers, and steel scalpels in general, plastic, gynecologic, urologic, and other open and endoscopic procedures.", "该设备可用作开放性和内窥镜手术中电外科手术、激光和钢制手术刀的辅助或替代工具，适用于普通外科、整形外科、妇科、泌尿科及其他手术。"),
            ("The device can be used to coagulate isolated vessels up to and including 7 mm in diameter using the minimum mode.", "使用最小模式时，该设备可用于凝闭最大 7 mm 直径的独立血管。"),
            ("The device can be used to coagulate isolated vessels up to and including 5 mm in diameter using the maximum mode.", "使用最大模式时，该设备可用于凝闭最大 5 mm 直径的独立血管。"),
            ("13 cm device is also indicated for use in otorhinolaryngologic (ENT) procedures.", "13 cm 设备亦适用于耳鼻喉科（ENT）手术。"),
        ]
    return []


def translate_file(input_path, output_path=None, src_lang='en', tgt_lang='zh'):
    """Translate a PPTX file in-place by extracting, translating XML, and repacking."""

    if output_path is None:
        stem = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{stem}-{tgt_lang}{Path(input_path).suffix}")

    translations = load_translations(src_lang, tgt_lang)

    # Work in a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract
        with zipfile.ZipFile(input_path, 'r') as z:
            z.extractall(tmpdir)

        # Find and translate all slide XML files
        slides_dir = Path(tmpdir) / 'ppt' / 'slides'
        if slides_dir.exists():
            for slide_file in sorted(slides_dir.glob('slide*.xml')):
                translated = translate_xml(str(slide_file), translations)
                if translated:
                    print(f"Translated: {slide_file.name}")

        # Also translate chart files if present
        for chart_file in Path(tmpdir).rglob('*.xml'):
            if translate_xml(str(chart_file), translations):
                pass  # silent

        # Repack into PPTX
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for fpath in Path(tmpdir).rglob('*'):
                if fpath.is_file():
                    arcname = fpath.relative_to(tmpdir)
                    zout.write(fpath, arcname)

    print(f"Output saved to: {output_path}")
    return output_path


def translate_xml(xml_path, translations):
    """Translate all text nodes in an XML file."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    modified = False

    for elem in root.iter():
        if elem.tag.endswith('}t') and elem.text:
            text = elem.text
            for eng, chn in translations:
                if eng in text:
                    text = text.replace(eng, chn)
            if text != elem.text:
                elem.text = text
                modified = True

    if modified:
        tree.write(xml_path, xml_declaration=True, encoding='UTF-8')

    return modified


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate PPTX files')
    parser.add_argument('input', help='Input PPTX file path')
    parser.add_argument('--output', '-o', help='Output PPTX file path')
    parser.add_argument('--src-lang', default='en', help='Source language code')
    parser.add_argument('--tgt-lang', default='zh', help='Target language code')
    args = parser.parse_args()

    translate_file(args.input, args.output, args.src_lang, args.tgt_lang)