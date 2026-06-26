from PIL import Image
import os
import sys

def merge_a4_to_a3(folder, output, dpi=300):
    """
    Merge images into A3 landscape PDF (two A4 images side by side).
    Images are sorted numerically and placed 2 per page.
    """
    # Get images sorted by number
    images = []
    for i in range(1, 1000):
        path = os.path.join(folder, f"{i}.jpg")
        if os.path.exists(path):
            images.append(path)
        elif i == 1 and not images:
            # Try other extensions if no jpg
            for ext in ['.png', '.jpeg', '.JPG', '.PNG']:
                path = os.path.join(folder, f"{i}{ext}")
                if os.path.exists(path):
                    images.append(path)
                    break
    
    if not images:
        print("No images found")
        return False
    
    # A3 landscape at 300 DPI: 4961 x 3508 pixels (420mm x 297mm)
    page_w = int(11.69 * dpi)   # A3 width
    page_h = int(8.27 * dpi)    # A3 height
    a4_w = page_w // 2          # Each A4 is half width
    a4_h = page_h               # Full height
    
    pdf_images = []
    for i in range(0, len(images), 2):
        page = Image.new('RGB', (page_w, page_h), 'white')
        
        # Left A4 (image 1)
        if i < len(images):
            img1 = Image.open(images[i]).convert('RGB')
            img1 = img1.resize((a4_w, a4_h), Image.LANCZOS)
            page.paste(img1, (0, 0))
            img1.close()
        
        # Right A4 (image 2)
        if i + 1 < len(images):
            img2 = Image.open(images[i + 1]).convert('RGB')
            img2 = img2.resize((a4_w, a4_h), Image.LANCZOS)
            page.paste(img2, (a4_w, 0))
            img2.close()
        
        pdf_images.append(page)
    
    if pdf_images:
        pdf_images[0].save(
            output,
            save_all=True,
            append_images=pdf_images[1:],
            dpi=(dpi, dpi),
            quality=100,
            subsampling=0
        )
        print(f"PDF created: {output}")
        print(f"Total pages: {len(pdf_images)}")
        print(f"Page size: A3 Landscape ({page_w}x{page_h} px @ {dpi} DPI)")
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        folder = sys.argv[1]
        output = sys.argv[2]
        dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    else:
        print("Usage: python merge_a4_to_a3.py <folder> <output.pdf> [dpi]")
        sys.exit(1)
    
    merge_a4_to_a3(folder, output, dpi)
