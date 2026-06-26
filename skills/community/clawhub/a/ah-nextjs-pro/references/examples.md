# Nextjs Pro — Code Examples

## Example 1

```tsx
// Server Component (default)
// app/products/page.tsx
import { Suspense } from 'react';
import { getProducts } from '@/lib/db';

export default async function ProductsPage({
  searchParams,
}: {
  searchParams: { category?: string; sort?: string };
}) {
  const products = await getProducts({
    category: searchParams.category,
    sort: searchParams.sort,
  });

  return (
    <div className="container">
      <Suspense fallback={<ProductsSkeleton />}>
        <ProductGrid products={products} />
      </Suspense>
    </div>
  );
}

// Client Component
// app/products/product-grid.tsx
'use client';

import { useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';

export function ProductGrid({ products }: { products: Product[] }) {
  const [isPending, startTransition] = useTransition();
  const router = useRouter();
  
  const handleFilter = (category: string) => {
    startTransition(() => {
      router.push(`/products?category=${category}`);
    });
  };

  return (
    <div className={isPending ? 'opacity-50' : ''}>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

## Example 2

```tsx
// app/actions/user.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';

const UpdateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function updateUser(userId: string, formData: FormData) {
  const validatedFields = UpdateUserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  try {
    await db.user.update({
      where: { id: userId },
      data: validatedFields.data,
    });

    revalidatePath('/profile');
    revalidateTag('user');
  } catch (error) {
    return { error: 'Failed to update user' };
  }

  redirect('/profile');
}

// Using Server Action in form
// app/profile/edit/page.tsx
export default function EditProfile({ user }: { user: User }) {
  const updateUserWithId = updateUser.bind(null, user.id);

  return (
    <form action={updateUserWithId}>
      <input name="name" defaultValue={user.name} />
      <input name="email" defaultValue={user.email} />
      <button type="submit">Update Profile</button>
    </form>
  );
}
```

## Example 3

```tsx
// Parallel data fetching
export default async function Dashboard() {
  const userPromise = getUser();
  const analyticsPromise = getAnalytics();
  const recentOrdersPromise = getRecentOrders();

  const [user, analytics, recentOrders] = await Promise.all([
    userPromise,
    analyticsPromise,
    recentOrdersPromise,
  ]);

  return (
    <>
      <UserProfile user={user} />
      <AnalyticsChart data={analytics} />
      <OrdersList orders={recentOrders} />
    </>
  );
}

// Streaming with Suspense
export default function Page() {
  return (
    <div>
      <Suspense fallback={<HeaderSkeleton />}>
        <Header />
      </Suspense>
      
      <Suspense fallback={<ContentSkeleton />}>
        <SlowLoadingContent />
      </Suspense>
      
      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar />
      </Suspense>
    </div>
  );
}

// Static generation with dynamic params
export async function generateStaticParams() {
  const posts = await getPosts();
  
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      images: [post.image],
    },
  };
}
```

## Example 4

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const category = searchParams.get('category');
  
  const posts = await getPosts({ category });
  
  return NextResponse.json(posts, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=30',
    },
  });
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  const { data, error } = await createPost(body);
  
  if (error) {
    return NextResponse.json({ error }, { status: 400 });
  }
  
  return NextResponse.json(data, { status: 201 });
}

// Streaming response
export async function GET() {
  const encoder = new TextEncoder();
  const stream = new TransformStream();
  const writer = stream.writable.getWriter();

  // Start streaming
  (async () => {
    for await (const chunk of generateContent()) {
      await writer.write(encoder.encode(chunk));
    }
    await writer.close();
  })();

  return new Response(stream.readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

## Example 5

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request });
  const isAuth = !!token;
  const isAuthPage = request.nextUrl.pathname.startsWith('/login');

  if (isAuthPage) {
    if (isAuth) {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
    return null;
  }

  if (!isAuth) {
    let from = request.nextUrl.pathname;
    if (request.nextUrl.search) {
      from += request.nextUrl.search;
    }

    return NextResponse.redirect(
      new URL(`/login?from=${encodeURIComponent(from)}`, request.url)
    );
  }
  
  // Add custom headers
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-user-id', token.sub);
  
  return NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/admin/:path*'],
};
```

## Example 6

```tsx
// Image optimization
import Image from 'next/image';

export function OptimizedImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero"
      width={1920}
      height={1080}
      priority
      placeholder="blur"
      blurDataURL={shimmer(1920, 1080)}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    />
  );
}

// Font optimization
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
});

// Dynamic imports
import dynamic from 'next/dynamic';

const DynamicChart = dynamic(() => import('@/components/chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});

// Lazy loading with Suspense
const LazyComponent = lazy(() => import('./heavy-component'));
```
