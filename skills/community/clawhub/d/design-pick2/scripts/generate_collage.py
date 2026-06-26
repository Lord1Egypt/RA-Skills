from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import textwrap

themes = {
    "Viral_Cakes": "VIRAL CAKES",
    "Street_Food": "STREET FOOD",
    "Smoothie_Bowls": "SMOOTHIE BOWLS",
    "Coffee_Art": "COFFEE ART",
    "Fusion_Tacos": "FUSION TACOS"
}

# Image configuration
img_size = 300
padding = 60
grid_size = 3
canvas_width = grid_size * img_size + (grid_size + 1) * padding
canvas_height = 250 + grid_size * (img_size + 120 + padding) + padding

for theme, title in themes.items():
    items = {}
    letters = "ABCDEFGHI"
    items_list = [
        "Chocolate Lava Cake", "Rainbow Layer Cake", "Red Velvet Cheesecake", 
        "Salted Caramel Drip Cake", "Matcha Mousse Cake", "Strawberry Shortcake", 
        "Cookie Dough Cake", "Tiramisu Cake", "Mango Passion Fruit Cake"
    ] if theme == "Viral_Cakes" else ([
        "Korean Corn Dog", "Street Taco", "Slider Burger", 
        "Falafel Wrap", "Banh Mi", "Tempura Shrimp", 
        "Loaded Fries", "Empanada", "Arancini"
    ] if theme == "Street_Food" else ([
        "Berry Acai Bowl", "Green Spinach Bowl", "Mango Coconut Bowl", 
        "Pitaya Dragonfruit Bowl", "Peanut Butter Banana Bowl", "Blue Spirulina Bowl", 
        "Chocolate Protein Bowl", "Kiwi Chia Bowl", "Mixed Fruit Bowl"
    ] if theme == "Smoothie_Bowls" else ([
        "Latte Heart Art", "Tulip Latte Art", "Rosetta Latte Art", 
        "Swan Latte Art", "Bear Foam Art", "Layered Iced Coffee", 
        "Caramel Macchiato", "Flat White", "Mocha Swirl Coffee"
    ] if theme == "Coffee_Art" else [
        "Korean BBQ Taco", "Spicy Shrimp Taco", "Tandoori Chicken Taco", 
        "Crispy Pork Belly Taco", "Vegetarian Mushroom Taco", "Steak Chimichurri Taco", 
        "Buffalo Cauliflower Taco", "Fish Tempura Taco", "Lamb Harissa Taco"
    ])))

    for i, label in enumerate(items_list):
        items[letters[i]] = (label, f"collages/{theme}/{letters[i]}.png")

    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    # Fonts
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(font_path, 80)
    label_font = ImageFont.truetype(font_path, 30)
    key_font = ImageFont.truetype(font_path, 70)

    # Dynamic Title based on theme
    title_text = "PICK 2 " + title if theme != "Smoothie_Bowls" else "PICK 3 " + title
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    draw.text(((canvas_width - (bbox[2] - bbox[0])) // 2, 40), title_text, fill="black", font=title_font)

    for i, (key, (label, path)) in enumerate(items.items()):
        row = i // grid_size
        col = i % grid_size
        
        img = Image.open(path).resize((img_size, img_size))
        
        # Create circular mask
        mask = Image.new('L', (img_size, img_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, img_size, img_size), fill=255)
        
        # Apply mask
        output = ImageOps.fit(img, (img_size, img_size), centering=(0.5, 0.5))
        output.putalpha(mask)
        
        x = padding + col * (img_size + padding)
        y = 250 + row * (img_size + 120 + padding)
        
        canvas.paste(output, (x, y), output)
        
        # Draw Key (A, B, C) outside top-left of image
        draw.text((x - 40, y - 40), key, fill="black", font=key_font)
        
        # Draw Multi-line Label
        lines = textwrap.wrap(label, width=15)
        for j, line in enumerate(lines):
            label_bbox = draw.textbbox((0, 0), line, font=label_font)
            draw.text((x + (img_size - (label_bbox[2] - label_bbox[0])) // 2, y + img_size + 10 + j*35), line, fill="black", font=label_font)

    canvas.save(f"collage_{theme}.png")
    print(f"Collage saved as collage_{theme}.png")
