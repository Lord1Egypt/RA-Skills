## Arcane Microframework Reference

### Philosophy: Location is Logic
Arcane minimizes configuration by using the filesystem. If you want a page, create a file. If you want a helper for a section, put it in that section's directory.

### Unified Primitives

#### `path()` Usage
- `path()`: Returns current URL.
- `path(1)`: Returns first URL segment.
- `path('/about')`: Normalizes to `/about/`.
- `path(['IMAGES', 'logo.svg'])`: Resolves to `/images/logo.svg`.
- `path('/file.php', true)`: Returns absolute server path.

#### `relay()` Usage
Used to pass data from a Page to a Layout.
```php
<?php relay('TITLE', 'Home'); ?>
<?php relay('SIDEBAR', function() { ?>
  <nav>...</nav>
<?php }); ?>
```

### Routing Validation
In `pages/blog.php`:
```php
<?php define('ROUTES', [
  ['history'],      // Matches /blog/history/
  [['2024', '2025']], // Matches /blog/2024/ or /blog/2025/
  ['*']             // Matches /blog/anything/
]);
```

### Autoload Cascade
For URL `/shop/checkout/`:
1. `helpers/*.php`
2. `helpers/shop/*.php`
3. `helpers/shop/checkout/*.php`
Specific helpers override general ones.

### Runtime Constants
- `CONTENT`: Rendered page HTML.
- `URI`: URL segments array.
- `PATH`: Resolved base path.
- `APP['ROOT']`: Web root.
- `STYLES` / `SCRIPTS`: Auto-generated HTML tags.
