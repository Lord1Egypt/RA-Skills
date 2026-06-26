#!/usr/bin/env python3
"""调试快手封面上传流程"""

from kbs.cdp import Browser
from kbs.types import load_publish_config
import time
import json

def debug_cover_upload():
    cfg = load_publish_config('../test_data/描述.txt')
    browser = Browser(host='127.0.0.1', port=9222)
    browser.connect()
    page = browser.get_or_create_page()
    
    print("=" * 60)
    print("步骤 1: 导航到上传页面")
    print("=" * 60)
    page.navigate('https://cp.kuaishou.com/article/publish/video')
    page.wait_for_load()
    time.sleep(3)
    print("✓ 页面加载完成\n")
    
    print("=" * 60)
    print("步骤 2: 上传视频")
    print("=" * 60)
    print(f"视频路径：{cfg.video_path}")
    page.set_file_input('input[type="file"]', [cfg.video_path])
    print("✓ 视频文件已设置")
    print("等待视频上传处理...")
    time.sleep(15)
    
    # 检查视频上传后的状态
    body_text = page.body_text()
    if '封面设置' in body_text:
        print("✓ 页面显示'封面设置'，视频上传成功\n")
    else:
        print("✗ 未找到'封面设置'，视频可能未上传成功\n")
    
    print("=" * 60)
    print("步骤 3: 上传前的页面分析")
    print("=" * 60)
    
    # 获取所有 file input
    file_inputs_info = page.evaluate('''
    () => {
        const inputs = document.querySelectorAll('input[type="file"]');
        const result = [];
        inputs.forEach((el, i) => {
            result.push({
                index: i,
                accept: el.accept.substring(0, 100),
                hasValue: el.files && el.files.length > 0
            });
        });
        return result;
    }
    ''')
    print(f"File input 数量：{len(file_inputs_info)}")
    print(f"详情：{json.dumps(file_inputs_info, indent=2, ensure_ascii=False)}\n")
    
    print("=" * 60)
    print("步骤 4: 点击封面设置")
    print("=" * 60)
    clicked = page.click_by_inner_text_then_center('封面设置')
    print(f"点击结果：{clicked}")
    time.sleep(2)
    
    # 检查点击后的变化
    file_inputs_after = page.evaluate('''
    () => {
        const inputs = document.querySelectorAll('input[type="file"]');
        const result = [];
        inputs.forEach((el, i) => {
            result.push({
                index: i,
                accept: el.accept.substring(0, 100),
                hasValue: el.files && el.files.length > 0,
                visible: el.offsetParent !== null
            });
        });
        return result;
    }
    ''')
    print(f"点击后 File input 数量：{len(file_inputs_after)}")
    print(f"详情：{json.dumps(file_inputs_after, indent=2, ensure_ascii=False)}\n")
    
    print("=" * 60)
    print("步骤 5: 上传封面文件")
    print("=" * 60)
    print(f"封面路径：{cfg.cover_path}")
    
    # 方法 1: 使用 accept hint
    print("\n尝试方法 1: set_file_input_by_accept_hint('image')")
    try:
        page.set_file_input_by_accept_hint('image', [cfg.cover_path])
        print("✓ 封面文件设置成功")
    except Exception as e:
        print(f"✗ 方法 1 失败：{e}")
    
    time.sleep(5)
    
    # 检查上传结果
    print("\n检查上传结果...")
    check_result = page.evaluate('''
    () => {
        const result = {
            fileInputs: [],
            blobImages: [],
            coverEditor: null
        };
        
        // 检查 file input
        const inputs = document.querySelectorAll('input[type="file"]');
        inputs.forEach((el, i) => {
            result.fileInputs.push({
                index: i,
                accept: el.accept.substring(0, 80),
                hasValue: el.files && el.files.length > 0,
                fileName: el.files && el.files.length > 0 ? el.files[0].name : null
            });
        });
        
        // 检查 blob 图片
        const imgs = document.querySelectorAll('img[src*="blob:"]');
        imgs.forEach((el, i) => {
            result.blobImages.push({
                src: el.src.substring(0, 100)
            });
        });
        
        // 检查封面编辑器
        const coverEditor = document.querySelector('._high-cover-editor_ps02t_1');
        if (coverEditor) {
            result.coverEditor = {
                exists: true,
                text: coverEditor.innerText.substring(0, 200)
            };
        }
        
        return result;
    }
    ''')
    
    print(f"\n上传结果：{json.dumps(check_result, indent=2, ensure_ascii=False)}")
    
    # 保存 HTML 用于分析
    html = page.evaluate('document.documentElement.outerHTML')
    with open('../test_data/debug_cover_result.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n✓ 页面 HTML 已保存到：../test_data/debug_cover_result.html")
    
    browser.close()
    print("\n" + "=" * 60)
    print("调试完成")
    print("=" * 60)

if __name__ == '__main__':
    debug_cover_upload()
