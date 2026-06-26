# AllProductsView

## Usage
```tsx
import { AllProductsView } from '@beyondcorp/beyond-ui';
import type { FilterOptions } from '@beyondcorp/beyond-ui/components/Marketplace/types';
import '@beyondcorp/beyond-ui/dist/styles.css';

const initialFilters: FilterOptions = {
  categories: [],
  brands: [],
  vendors: [],
  priceRange: [0, 1000],
  rating: 0,
  inStock: false,
};

export function ProductsPage() {
  const [filters, setFilters] = useState(initialFilters);
  const [query, setQuery] = useState('');

  return (
    <AllProductsView
      filters={filters}
      searchQuery={query}
      onFiltersChange={setFilters}
      onClearFilters={() => setFilters(initialFilters)}
      setSearchQuery={setQuery}
      onAddToCart={(product) => console.log('Add to cart', product)}
      onProductClick={(product) => console.log('Open product', product.id)}
    />
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| products | Product[] | Optional override (defaults to packaged sample data) |
| filters | FilterOptions | Active filter state (categories, brands, price, etc.) |
| searchQuery | string | Current search string |
| setSearchQuery | (query: string) => void | Update handler for search field |
| shouldFocusSearch | boolean | Autofocus search input when true |
| onFiltersChange | (filters: FilterOptions) => void | Called when filters change |
| onClearFilters | () => void | Resets filters; also resets pagination |
| onProductClick | (product: Product) => void | Triggered when listing card clicked |
| onAddToCart | (product: Product) => void | Hook into cart logic; shows toast by default |

## Notes
- Handles responsive grid/list layouts, wishlist toggles, quick view modals, and pagination.
- Provide your own products array or rely on bundled sample data for demos.
- Emits toast notifications via `showToast`; wrap `<Toast />` at the app root.

Story source: stories/AllProductsView.stories.tsx
