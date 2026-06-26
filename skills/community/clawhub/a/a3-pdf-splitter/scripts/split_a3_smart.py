import pypdfium2 as pdfium
from PIL import Image
import os
import sys

def find_best_split_position(img, is_horizontal=True):
    """
    智能寻找最佳切割位置：在中间区域寻找最空白的列/行
    is_horizontal=True：左右切（找最佳列）；False：上下切（找最佳行）
    """
    # 转为灰度图像
    gray_img = img.convert('L')
    pixels = list(gray_img.getdata())
    width, height = gray_img.size
    
    if is_horizontal:
        # 左右切：计算每列的像素和，和越大越空白（255是纯白色）
        middle_start = int(width * 0.45)
        middle_end = int(width * 0.55)
        max_sum = -1
        best_x = middle_start
        
        for x in range(middle_start, middle_end):
            col_sum = 0
            for y in range(height):
                col_sum += pixels[y * width + x]
            if col_sum > max_sum:
                max_sum = col_sum
                best_x = x
        return best_x
    else:
        # 上下切：计算每行的像素和
        middle_start = int(height * 0.45)
        middle_end = int(height * 0.55)
        max_sum = -1
        best_y = middle_start
        
        for y in range(middle_start, middle_end):
            row_sum = 0
            for x in range(width):
                row_sum += pixels[y * width + x]
            if row_sum > max_sum:
                max_sum = row_sum
                best_y = y
        return best_y

def split_a3_to_a4_smart(input_path, output_path):
    # 打开PDF文件
    pdf = pdfium.PdfDocument(input_path)
    output_images = []
    
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        width, height = page.get_size()
        
        # 渲染页面为高分辨率图像（400 DPI）
        scale = 400 / 72
        bitmap = page.render(scale=scale)
        img = bitmap.to_pil()
        
        # A3横向：左右切
        if width > height:
            split_x = find_best_split_position(img, is_horizontal=True)
            print(f"第{page_num+1}页最佳切割位置：x={split_x} (总宽度{img.width})")
            
            # 左半部分
            left_img = img.crop((0, 0, split_x, img.height))
            output_images.append(left_img)
            
            # 右半部分
            right_img = img.crop((split_x, 0, img.width, img.height))
            output_images.append(right_img)
        else:
            # A3纵向：上下切
            split_y = find_best_split_position(img, is_horizontal=False)
            print(f"第{page_num+1}页最佳切割位置：y={split_y} (总高度{img.height})")
            
            # 上半部分
            top_img = img.crop((0, 0, img.width, split_y))
            output_images.append(top_img)
            
            # 下半部分
            bottom_img = img.crop((0, split_y, img.width, img.height))
            output_images.append(bottom_img)
    
    # 保存为PDF
    if output_images:
        output_images[0].save(
            output_path,
            "PDF",
            resolution=400,
            save_all=True,
            append_images=output_images[1:]
        )
    
    print(f"\n处理完成！输出文件：{output_path}")
    print(f"原始页数：{len(pdf)}，切分后页数：{len(output_images)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python split_a3_smart.py <输入PDF路径> <输出PDF路径>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"错误：输入文件 {input_file} 不存在")
        sys.exit(1)
    
    split_a3_to_a4_smart(input_file, output_file)