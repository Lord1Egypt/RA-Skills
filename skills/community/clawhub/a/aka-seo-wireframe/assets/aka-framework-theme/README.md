# AKA Framework WordPress Theme

Simple, clean WordPress theme optimized for the **AKA (Authority-Knowledge-Answer)** framework.

## Features

### Three Custom Page Templates
- **Authority Hub** - Main hub pages with child navigation
- **Knowledge Page** - Deep-dive content with related topics
- **Answer Page** - FAQ format optimized for featured snippets

### Built-in Components
- ✅ Breadcrumbs navigation
- ✅ Related topics/questions
- ✅ Quick navigation for hubs
- ✅ CTA boxes
- ✅ Mobile-responsive design
- ✅ SEO-optimized structure
- ✅ Clean, minimal design

### Easy Customization
- CSS variables for colors/spacing
- WordPress Customizer support
- Custom logo support
- Multiple navigation menus
- Widget-ready footer

## Installation

### Option 1: Upload via WordPress Admin
1. Go to **Appearance → Themes → Add New**
2. Click **Upload Theme**
3. Choose the `aka-framework-theme.zip` file
4. Click **Install Now**
5. Activate the theme

### Option 2: Manual Installation
1. Upload the `aka-framework-theme` folder to `/wp-content/themes/`
2. Go to **Appearance → Themes**
3. Activate **AKA Framework Theme**

## Usage

### Creating an Authority Hub

1. Create a new page in WordPress
2. Assign **Authority Hub** template
3. This becomes your main hub page
4. All child pages will appear in the quick navigation

### Creating Knowledge Pages

1. Create a new page
2. Set parent to your Authority Hub
3. Assign **Knowledge Page** template
4. Related sibling knowledge pages will auto-link

### Creating Answer Pages

1. Create a new page
2. Set parent to your Authority Hub
3. Assign **Answer Page** template
4. Use the excerpt for the "Quick Answer" box (featured snippet optimization)
5. Related questions will auto-link

## Page Structure Example

```
Authority Hub: Atlanta Car Accident Lawyer
├── Knowledge: Types of Car Accident Claims
├── Knowledge: Georgia Car Accident Laws
├── Knowledge: Insurance Claims Process
├── Answer: How long do I have to file a claim?
├── Answer: What is my case worth?
└── Answer: Do I need a lawyer?
```

## Customization

### Change Colors

**Method 1: WordPress Customizer**
- Go to **Appearance → Customize → Colors**
- Change Primary Color

**Method 2: Edit CSS Variables** (in `style.css`)
```css
:root {
  --primary-color: #2563eb;    /* Your brand color */
  --secondary-color: #1e40af;  /* Darker shade */
  --accent-color: #f59e0b;     /* Call-to-action color */
}
```

### Add Phone Number

1. Go to **Appearance → Customize**
2. Find "Phone Number" setting
3. Enter your phone number
4. It will appear in the footer

### Navigation Menus

Create two menus:
- **Primary Menu** - Main navigation (header)
- **Footer Menu** - Footer links

Go to **Appearance → Menus** to create them.

## File Structure

```
aka-framework-theme/
├── style.css                 # Main stylesheet with all CSS
├── functions.php             # Theme functions and helpers
├── header.php                # Site header
├── footer.php                # Site footer
├── index.php                 # Fallback template
├── page-authority-hub.php    # Authority Hub template
├── page-knowledge.php        # Knowledge Page template
├── page-answer.php           # Answer Page template
└── README.md                 # This file
```

## Theme Functions

The theme includes helper functions you can use in templates:

```php
// Get hub navigation (child pages)
echo aka_get_hub_navigation();

// Get breadcrumbs
echo aka_get_breadcrumbs();

// Get related topics
echo aka_get_related_topics();

// Get related questions
echo aka_get_related_questions();

// Display CTA box
echo aka_get_cta_box( 'Title', 'Description', 'Button Text', 'Button URL' );
```

## CSS Classes

Utility classes available:

```css
.text-center, .text-left, .text-right   /* Text alignment */
.mt-sm, .mt-md, .mt-lg                  /* Margin top */
.mb-sm, .mb-md, .mb-lg                  /* Margin bottom */
```

## Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Requirements

- WordPress 5.0 or higher
- PHP 7.4 or higher

## License

MIT License - Free for personal and commercial use

## Support

For issues or questions:
- GitHub: https://github.com/lebtiga/aka-wireframe-wp-system
- Documentation: See AKA-WIREFRAME-WP-COMPLETE.md

## Changelog

### Version 1.0.0
- Initial release
- Three custom page templates
- Mobile-responsive design
- SEO optimized structure
- Basic customization options

---

Built specifically for the AKA Wireframe WordPress system.
