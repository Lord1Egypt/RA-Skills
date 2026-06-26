# Divar.ir API Skills Documentation

## Overview
Comprehensive API documentation for Divar.ir's real estate marketplace, extracted from browser developer tools. This skill provides complete reference for building applications that interact with Divar's widget-based API.

## Key Components

### Architecture
- **Widget-based API**: Server-driven UI with typed widgets
- **Protocol Buffers**: Type annotations via `@type` field
- **Session Authentication**: Cookie-based auth required
- **JSON Protocol**: All endpoints use JSON over HTTPS

### Core Endpoints
1. **Search & Listings** (`/v8/postlist/w/search`)
   - Paginated search results with cursor-based pagination
   - Widget-based response structure
   - Support for complex search criteria

2. **Post Details** (`/v8/posts-v2/web/{token}`)
   - Full post detail pages with sections
   - Rich widget content (images, maps, descriptions)
   - Contact information widgets

3. **Contact Info** (`/v8/postcontact/web/contact_info_v2/{token}`)
   - Seller contact details
   - Phone numbers with copy functionality
   - Security warnings about fraud

4. **Map Clustering** (`/v8/mapview/viewport`)
   - Geo-clustered listings
   - Custom tile servers
   - Zoom-based density calculations

5. **Autocomplete** (`/v8/prediction/w/query`)
   - Real-time search suggestions
   - Category-based predictions
   - Ad count indicators

6. **Dynamic Filters** (`/v8/postlist/w/filters`)
   - District multi-select
   - Price range and size filters
   - Lazy-loaded filter options

### Widget System
All API responses use structured widgets:
- `POST_ROW` - Listing cards in search results
- `KEY_VALUE` - Property detail rows
- `IMAGE_GALLERY` - Photo galleries
- `MAP` - Embedded interactive maps
- `UNEXPANDABLE_ROW` - Contact information
- `BREADCRUMB` - Navigation breadcrumbs
- `STATEMENT` - Warning/information blocks

### Pagination Pattern
- Cursor-based pagination using timestamps
- Bloom filters for deduplication
- Persistent search UUID across sessions
- Cumulative widget counting

### Category Support
- Real estate sales and rentals
- Commercial and residential properties
- Short-term rentals
- Construction services
- Persian localization support

### Infrastructure
- **API Version**: v8 (stable)
- **Map Tiles**: Custom servers (tiles.raah.ir, map.divarcdn.com)
- **CDN Assets**: WebP images with thumbnails
- **Error Monitoring**: Sentry integration
- **Analytics**: Multiple beacon endpoints for tracking

## Usage Notes
- Requires authenticated session cookies
- Cross-origin requests blocked (CORS restrictions)
- Widget actions trigger client-side navigation
- Protocol Buffers types embedded in JSON
- Persian text and Farsi localization fully supported

## Authentication
All authenticated endpoints require session cookies. Unauthenticated calls return `RBAC: access denied` errors. Login must be performed through the web interface to obtain valid session cookies.

## Rate Limiting
No explicit rate limiting documented, but excessive requests may trigger bot detection. Implement proper delays between requests and respect server response times.

## Error Handling
- Monitor Sentry error tracking (sentry.divar.cloud)
- Check response status codes
- Handle pagination token expiration
- Graceful degradation for missing widgets

## Integration Tips
- Use widget actions for navigation
- Implement proper error boundaries
- Cache responses where appropriate
- Respect user privacy and data handling
- Follow Iranian real estate regulations when building applications