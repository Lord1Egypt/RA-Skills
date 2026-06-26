import { NextResponse } from 'next/server';
import { isDemoMode } from '@/lib/demo-data';

export async function GET() {
  return NextResponse.json({ mode: isDemoMode() ? 'demo' : 'live' });
}
