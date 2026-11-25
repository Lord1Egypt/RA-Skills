import { getDb } from '@/lib/db';

export const dynamic = 'force-dynamic';

// Health check for the platform: read-only database check, no business logic.
export function GET() {
  getDb().prepare('SELECT 1').get();
  return Response.json({ status: 'ok' });
}
