## BCMS Media

The media library stores images and other files used across entries and templates.
BCMS automatically generates multiple image sizes for responsive delivery.

---

### Uploading media (Dashboard)

To upload a file:

1. Go to the **Media** section in the sidebar.
2. Click **Upload file** or drag & drop into the upload area.
3. Choose a file from your system.

For images, BCMS stores the original and generates several resized variants for performance.

---

### Folders and organisation

- Click **Create new folder** to create folders.
- New folders are created inside the current folder (supporting nesting).
- Uploads respect the active folder path, similar to a filesystem.

Use folders to separate content types (e.g. `blog`, `products`, `avatars`).

---

### Renaming and deleting media

- To rename a file:
  1. Hover over the media item.
  2. Click the pencil icon.
  3. Enter a new name and save.

- To delete a file or folder:
  1. Open the dropdown menu on the item.
  2. Select **Delete**.

⚠️ Deleting media removes it from any entries and widgets where it is used.
Always check usage before deleting in production projects.

---

### Media and `BCMSContentManager`

`<BCMSContentManager />` can automatically render image nodes inside rich‑text content.
It chooses an appropriate size based on layout and screen size.

For React:

```tsx
import { BCMSContentManager } from '@thebcms/components-react';

<BCMSContentManager
  items={post.content.en}
  clientConfig={bcms.getConfig()}
/>;
```

Currently, only images are auto‑rendered; video/PDF/other file types are not handled by `BCMSContentManager` and should be rendered manually using the media data.

---

### Auto‑generated sizes for images

When you upload an image, BCMS generates multiple width‑based versions, typically:

- 350 px
- 600 px
- 900 px
- 1200 px
- 1600 px
- 1920 px

When rendering images with `BCMSImage`, the component automatically selects the closest suitable size based on rendered dimensions, balancing performance and quality.

---

### Dedicated media API key

Because media often needs to be accessed from the public frontend, it’s common to use a **dedicated media API key** with limited permissions.

Example client:

```ts
import { Client } from '@thebcms/client';

// Use a dedicated public three-part media key (env name per your app; mirrors NEXT_PUBLIC_BCMS_API_KEY style)
export const bcmsMediaClient = new Client({
  apiKey: process.env.NEXT_PUBLIC_BCMS_MEDIA_API_KEY!,
  injectSvg: true,
});
```

Benefits:

- Granular permissions (limit key to media).
- Separation of concerns (one key for content management, another for media).
- Reduced impact if the key is exposed.

---

### Typical operations (SDK)

- List files or folders: `bcms.media.getAll()`
- Get a specific file: `bcms.media.getById(id)`
- Create directories and upload files (see `scripts/upload-media.ts`).

More detailed examples:

```ts
// Get all media
const allMedia = await bcms.media.getAll();

// Get a single media file
const media = await bcms.media.getById('media_id');

// Get binary buffer (e.g. image)
const fileBuffer = await media.bin();

// Get thumbnail
const thumbnailBuffer = await media.thumbnail();

// Build a public URI
const uri = bcms.media.toUri('media_id', 'filename.jpg', { webp: true });

// Create a folder
await bcms.media.createDir({ name: 'images', parentId: 'folder_id' });

// Request upload token and upload a file
const uploadToken = await bcms.media.requestUploadToken();

await bcms.media.createFile({
  uploadToken,
  name: 'logo.png',
  file: yourFileBlob,
});
```

---

### Best‑practices

- Use **dedicated media API keys** with limited permissions for public delivery.
- Compress and optimise images before upload when possible.

---

See the official BCMS media documentation for supported formats, limits and optimisation strategies.
