# -*- coding: utf-8 -*-
"""
腾讯混元AI批量图生图自动化脚本
用于 timiai.woa.com 平台的批量参考生图任务

功能：
- 批量上传参考图片
- 自动生成AI图片
- 自动下载生成的图片
- 支持每张图片多次生成
- 自动命名保存
"""

import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime
import time
import sys
import requests
import glob

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


async def main():
    # ==================== 配置区域 ====================
    # 请根据需要修改以下参数
    
    # 源文件夹路径（包含参考图片）
    source_folder = r"C:\Users\Rubinnsun\Desktop\五五开黑\镜头制作-二分\0403"
    
    # 生成关键词（风格描述）
    keyword = """图一参考图二优化光影，优化二分色，光源为逆光，不要改变图一的人物 不要改变原图内容，不重设计，不重构图，不重摆角色，不改变服装颜色方案，不改变人物年龄感，不改变镜头语言。只修正这一帧的二分色问题和光影完成度：统一主光方向，提升角色亮面与暗面的清晰度，减少软糊渐变和脏灰过渡，让脸、头发、脖子、手部、胸口、衣袖、获得更明确的大块切面。压缩中间灰，增加图形化明暗组织，让角色从背景中更有力地跳出来。背景保留氛围即可，建筑、人群和地面纹理适度简化，避免信息量分散主体注意力。整体结果要求更像专业动画色指定与摄影修正后的成片单帧，干净、明确、利落、统一。 负面限制：不要重绘成厚涂插画，不要添加复杂纹理，不要增加写实皮肤，不要加重磨皮感，不要把白色区域涂脏，不要把背景做得比角色更亮。 咒术回战风格，具有浓郁二次元风格的插画，画面充满梦幻、浪漫氛围。画面色彩绚丽，光影效果细腻，造型优美，充满幻想和浪漫元素，新海诚色彩，光影丰富，画面丰富，温馨治愈，整体画面呈现出极致精美的视觉效果，杜绝任何模糊或失真，，动画电影摄影质感，动画电影的效果。动画电影级镜头质感，画面暗部色彩通透，光感，高清，4K画质，最佳品质，超精细，镜头光晕，光影层次感，肌理反光，材质反射，艺术氛围，情绪表达和叙事，高级的氛围感，场景空间感，层次感，8K高清、大师作品"""
    
    # 每张图片生成的次数
    generations_per_image = 5
    
    # ==================== 以下代码无需修改 ====================
    
    # 自动生成保存文件夹名：源文件夹名 + 日期 + AI
    source_folder_name = os.path.basename(source_folder.rstrip(os.sep))
    today_date = datetime.now().strftime("%m%d")
    save_folder_name = f"{source_folder_name}_{today_date}AI"
    parent_dir = os.path.dirname(source_folder.rstrip(os.sep))
    save_folder = os.path.join(parent_dir, save_folder_name)
    
    print(f"[配置] 源文件夹: {source_folder}")
    print(f"[配置] 保存文件夹: {save_folder}")
    print(f"[配置] 每张图片生成次数: {generations_per_image}")
    
    # 创建保存文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"[创建] 保存文件夹: {save_folder}\n")
    
    # 获取所有图片文件
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.webp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(source_folder, ext)))
    
    if not image_files:
        print("[错误] 源文件夹中没有找到图片文件！")
        return
    
    print(f"[发现] 共找到 {len(image_files)} 张图片")
    for i, img_path in enumerate(image_files, 1):
        filename = os.path.basename(img_path)
        print(f"  {i}. {filename}")
    
    print(f"\n{'='*60}")
    print(f"开始批量图生图生成")
    print(f"{'='*60}\n")
    
    async with async_playwright() as p:
        user_data_dir = os.path.join(os.path.expanduser("~"), ".timiai_browser_data")
        
        print("[启动] 启动浏览器...")
        browser = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 1920, "height": 1080},
            args=['--start-maximized']
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # 访问 timiai
        print("[访问] 打开 timiai.woa.com...")
        try:
            await page.goto("https://timiai.woa.com/image-generation", wait_until="load", timeout=60000)
        except:
            print("[警告] 页面加载超时，尝试继续...")
        await asyncio.sleep(5)
        
        # 步骤1：切换到"参考生图"模式
        print("\n[步骤1] 切换到'参考生图'模式...")
        try:
            reference_btn = await page.query_selector('text="参考生图"')
            if reference_btn:
                await reference_btn.click()
                print("[OK] 已点击'参考生图'")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"[警告] 点击参考生图失败: {e}")
        
        # 处理每张图片
        file_counter = 0
        for image_path in image_files:
            original_name = os.path.splitext(os.path.basename(image_path))[0]
            
            # 每张图片生成多次
            for gen_num in range(1, generations_per_image + 1):
                file_counter += 1
                print(f"\n{'='*60}")
                print(f"[处理 {file_counter}/{len(image_files) * generations_per_image}] {original_name} - 第{gen_num}次生成")
                print(f"{'='*60}\n")
                
                # 生成目标文件名
                target_filename = f"{original_name}_{file_counter:03d}.png"
                target_path = os.path.join(save_folder, target_filename)
                
                # 检查是否已存在
                if os.path.exists(target_path):
                    print(f"[跳过] 文件已存在: {target_filename}")
                    continue
                
                try:
                    # 步骤2：清空所有旧的参考图片
                    print(f"[步骤2] 清空所有旧的参考图片...")
                    
                    deleted_count = 0
                    max_delete_attempts = 10
                    
                    for attempt in range(max_delete_attempts):
                        # 先关闭可能存在的图片查看器弹窗
                        viewer_close = await page.query_selector('.el-image-viewer__close, [class*="viewer"] [class*="close"]')
                        if viewer_close:
                            try:
                                await viewer_close.click(timeout=1000)
                                print(f"  [关闭] 图片查看器弹窗")
                                await asyncio.sleep(0.5)
                            except:
                                pass
                        
                        try:
                            # 查找参考图片容器
                            containers = await page.query_selector_all('[class*="image-item"]')
                            
                            # 过滤出有实际图片的容器
                            valid_containers = []
                            for container in containers:
                                img = await container.query_selector('img:not(.el-image-viewer__img)')
                                if img:
                                    src = await img.get_attribute('src')
                                    if src and len(src) > 50:
                                        valid_containers.append(container)
                            
                            if not valid_containers:
                                print(f"[完成] 没有更多参考图需要删除，共清空 {deleted_count} 张")
                                break
                            
                            # 只处理第一个容器
                            container = valid_containers[0]
                            
                            # 悬停在 image-mask 遮罩层上
                            mask = await container.query_selector('.image-mask, [class*="image-mask"]')
                            
                            if mask:
                                await mask.hover(timeout=3000)
                                await asyncio.sleep(0.5)
                                
                                # 查找所有图标（有2个：放大镜和垃圾桶）
                                delete_icons = await container.query_selector_all('.mask-icon, [class*="mask-icon"]')
                                
                                # 点击第二个图标（垃圾桶）
                                if len(delete_icons) >= 2:
                                    delete_icon = delete_icons[1]
                                    try:
                                        await delete_icon.click(timeout=2000)
                                        deleted_count += 1
                                        print(f"  [OK] 已删除第 {deleted_count} 张参考图")
                                        await asyncio.sleep(1)
                                    except Exception as e:
                                        print(f"  [点击失败] {e}")
                                elif len(delete_icons) == 1:
                                    try:
                                        await delete_icons[0].click(timeout=2000)
                                        deleted_count += 1
                                        print(f"  [OK] 已删除第 {deleted_count} 张参考图")
                                        await asyncio.sleep(1)
                                    except:
                                        pass
                            else:
                                print(f"  [提示] 未找到遮罩层，可能已清空")
                                break
                                
                        except Exception as e:
                            print(f"  [警告] 删除过程中出错: {e}")
                            break
                    
                    # 如果删除数量为0，使用刷新页面作为兜底方案
                    if deleted_count == 0:
                        print(f"[提示] 未找到可删除的参考图，刷新页面确保清空...")
                        await page.reload(wait_until="networkidle")
                        await asyncio.sleep(5)
                        
                        # 重新切换到参考生图模式
                        print(f"[操作] 重新切换到'参考生图'模式...")
                        try:
                            reference_btn = await page.query_selector('text="参考生图"')
                            if not reference_btn:
                                reference_btn = await page.query_selector('button:has-text("参考生图")')
                            if not reference_btn:
                                reference_btn = await page.query_selector('[class*="参考生图"]')
                            
                            if reference_btn:
                                await reference_btn.click()
                                print(f"[OK] 已重新切换到'参考生图'模式")
                                await asyncio.sleep(3)
                            else:
                                print(f"[警告] 未找到'参考生图'按钮，尝试继续...")
                        except Exception as e:
                            print(f"[警告] 切换到参考生图失败: {e}")
                    
                    await asyncio.sleep(1)
                    
                    # 步骤3：上传新的参考图片
                    print(f"\n[步骤3] 上传新的参考图片...")
                    print(f"  源文件: {image_path}")
                    
                    file_input = await page.query_selector('input[type="file"]')
                    
                    if not file_input:
                        all_inputs = await page.query_selector_all('input')
                        print(f"[调试] 找到 {len(all_inputs)} 个input元素")
                        for i, inp in enumerate(all_inputs):
                            input_type = await inp.get_attribute('type')
                            print(f"  {i+1}. type='{input_type}'")
                            if input_type == 'file':
                                file_input = inp
                                break
                    
                    if file_input:
                        await file_input.set_input_files(image_path)
                        print(f"[OK] 已上传图片")
                        await asyncio.sleep(5)
                    else:
                        print(f"[警告] 未找到文件上传input")
                        continue
                    
                    # 步骤4：输入关键词
                    print(f"\n[步骤4] 输入关键词...")
                    textarea = await page.query_selector('textarea[placeholder*="描述"], textarea')
                    if textarea:
                        await textarea.fill("")
                        await asyncio.sleep(0.3)
                        await textarea.fill(keyword)
                        print(f"[OK] 关键词已输入")
                        await asyncio.sleep(1)
                    
                    # 步骤5：选择"自适应"图片比例
                    print(f"\n[步骤5] 选择图片比例为'自适应'...")
                    try:
                        adaptive_btn = await page.query_selector('text="自适应"')
                        if adaptive_btn:
                            await adaptive_btn.click()
                            print(f"[OK] 已选择'自适应'")
                            await asyncio.sleep(1)
                    except Exception as e:
                        print(f"[警告] 选择自适应失败: {e}")
                    
                    # 步骤6：选择清晰度为"4K高清"
                    print(f"\n[步骤6] 选择清晰度为'4K高清'...")
                    try:
                        clarity_btn = await page.query_selector('text="4K高清"')
                        if clarity_btn:
                            await clarity_btn.click()
                            print(f"[OK] 已选择'4K高清'")
                            await asyncio.sleep(1)
                    except Exception as e:
                        print(f"[警告] 选择4K高清失败: {e}")
                    
                    # 步骤7：点击生成
                    print(f"\n[步骤7] 点击生成按钮...")
                    
                    # 记录生成前的URL（用于后续验证）
                    pre_generate_urls = set()
                    try:
                        imgs = await page.query_selector_all('img')
                        for img in imgs:
                            src = await img.get_attribute('src')
                            if src and len(src) > 50:
                                pre_generate_urls.add(src)
                    except:
                        pass
                    
                    gen_btn = await page.query_selector('button:has-text("生成")')
                    if gen_btn:
                        await gen_btn.evaluate('el => el.scrollIntoView({block: "center"})')
                        await asyncio.sleep(1)
                        await gen_btn.click()
                        print(f"[OK] 已点击生成")
                    else:
                        print(f"[警告] 未找到生成按钮")
                        continue
                    
                    # 步骤8：等待生成完成
                    print(f"\n[步骤8] 等待图片生成（30-120秒）...")
                    await asyncio.sleep(10)
                    
                    max_wait = 180
                    start_time = time.time()
                    latest_image_url = None
                    latest_image_size = 0
                    
                    while time.time() - start_time < max_wait:
                        try:
                            imgs = await page.query_selector_all('img')
                            for img in imgs:
                                src = await img.get_attribute('src')
                                if not src or len(src) < 50:
                                    continue
                                
                                if src in pre_generate_urls:
                                    continue
                                
                                box = await img.bounding_box()
                                if box and box['width'] > 300 and box['height'] > 300:
                                    area = box['width'] * box['height']
                                    if area > latest_image_size:
                                        latest_image_size = area
                                        latest_image_url = src
                                        print(f"[发现] 新生成图片: {int(box['width'])}x{int(box['height'])}")
                        except:
                            pass
                        
                        if latest_image_size > 500000:
                            print(f"[等待] 检测到大图，等待生成完成...")
                            await asyncio.sleep(15)
                            break
                        
                        await asyncio.sleep(2)
                        elapsed = int(time.time() - start_time)
                        if elapsed % 10 == 0:
                            print(f"[等待] {elapsed}秒...")
                    
                    if not latest_image_url:
                        print(f"[失败] 未检测到新生成的图片")
                        continue
                    
                    # 步骤9：下载图片
                    print(f"\n[步骤9] 下载图片...")
                    print(f"  目标文件名: {target_filename}")
                    print(f"  图片URL: {latest_image_url[:80]}...")
                    
                    try:
                        print(f"[方法] 使用requests直接下载图片URL...")
                        
                        cookies = await page.context.cookies()
                        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                        
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'Referer': 'https://timiai.woa.com/',
                        }
                        
                        response = requests.get(latest_image_url, cookies=cookies_dict, headers=headers, timeout=60)
                        
                        if response.status_code == 200:
                            content_type = response.headers.get('Content-Type', '')
                            print(f"  Content-Type: {content_type}")
                            print(f"  文件大小: {len(response.content)/1024:.1f}KB")
                            
                            with open(target_path, 'wb') as f:
                                f.write(response.content)
                            
                            size = os.path.getsize(target_path)
                            print(f"[成功] 已保存: {target_filename} ({size/1024:.1f}KB)")
                            
                            # 步骤10：验证下载的图片
                            print(f"\n[步骤10] 验证图片...")
                            verify_size = os.path.getsize(target_path)
                            print(f"  文件大小: {verify_size/1024:.1f}KB")
                            
                            if verify_size < 50000:
                                print(f"[警告] 文件太小，可能下载失败")
                            else:
                                print(f"[OK] 图片验证通过")
                        else:
                            print(f"[失败] HTTP状态码: {response.status_code}")
                        
                    except Exception as e:
                        print(f"[错误] 下载过程中出错: {e}")
                        import traceback
                        traceback.print_exc()
                    
                    await asyncio.sleep(3)
                    
                except Exception as e:
                    print(f"[错误] 处理图片时出错: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
        
        print(f"\n{'='*60}")
        print(f"[完成] 批量图生图生成完成")
        print(f"{'='*60}")
        print(f"\n保存位置: {save_folder}")
        
        generated_files = glob.glob(os.path.join(save_folder, "*.png"))
        print(f"\n共生成 {len(generated_files)} 个文件:")
        for f in sorted(generated_files):
            size = os.path.getsize(f)
            print(f"  - {os.path.basename(f)} ({size/1024:.1f}KB)")
        
        print("\n[提示] 浏览器保持打开，可手动检查")
        await asyncio.sleep(30)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
