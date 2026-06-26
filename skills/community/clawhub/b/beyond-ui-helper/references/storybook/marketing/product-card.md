# ProductCard

## Usage
```tsx
import { ProductCard } from '@beyondcorp/beyond-ui';
import type { Product } from '@beyondcorp/beyond-ui/components/Marketplace/types';
import '@beyondcorp/beyond-ui/dist/styles.css';

const product: Product = {
  id: 'sku-101',
  name: 'Wireless Headphones',
  brand: 'Sony',
  description: 'High-quality wireless headphones with noise cancellation.',
  price: 199.99,
  originalPrice: 249.99,
  discount: 20,
  rating: 4.7,
  reviewCount: 128,
  images: ['https://images.pexels.com/photos/374870/pexels-photo-374870.jpeg?auto=compress&w=400'],
  category: 'electronics',
  vendor: { id: 'vendor-1', name: 'TechWorld Store', rating: 4.8 },
  inStock: true,
  specifications: {},
  tags: [],
};

export function FeaturedProduct() {
  return (
    <ProductCard
      product={product}
      isWishlisted={false}
      onAddToCart={(item) => console.log('Add to cart', item.id)}
      onProductClick={(item) => console.log('View product', item.id)}
      onQuickView={(item) => console.log('Quick view', item.id)}
      onToggleWishlist={(item) => console.log('Toggle wishlist', item.id)}
    />
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| product | Product | Product data record (pricing, images, vendor, etc.) |
| isWishlisted | boolean | Marks card as saved by the user |
| showQuickActions | boolean | Toggles quick view/wishlist/cart buttons |
| onProductClick | (product: Product) => void | Fired when card or CTA clicked |
| onQuickView | (product: Product) => void | Opens modal preview |
| onAddToCart | (product: Product) => void | Hook into cart logic |
| onToggleWishlist | (product: Product) => void | Persist wishlist state |
| className | string | Extend outer wrapper classes |

## Notes
- Displays discount badge, rating stars, and stock badge automatically from `product` data.
- Responsive layout scales from mobile to desktop; wrap in grid or carousels for catalog pages.
- Share toast context (`<Toast />`) if triggering add-to-cart feedback alongside AllProductsView.

Story source: stories/ProductCard.stories.tsx
