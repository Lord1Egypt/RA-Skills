import { NextResponse } from 'next/server'

export const config = {
  matcher: ['/((?!api|_next|.*\\..*).*)']
}

export function middleware(req) {
  const { pathname } = req.nextUrl
  if (pathname === '/') {
    return NextResponse.redirect(new URL('/zh', req.url))
  }
  return NextResponse.next()
}
