import { getDb } from '@/lib/db';

export const dynamic = 'force-dynamic';

export function GET() {
  return Response.json(getDb().prepare('SELECT * FROM todos ORDER BY id').all());
}

export async function POST(req: Request) {
  const { title } = (await req.json()) as { title?: string };
  if (!title?.trim()) return Response.json({ error: 'title required' }, { status: 400 });
  const r = getDb().prepare('INSERT INTO todos (title, created_at) VALUES (?, ?)').run(title.trim().slice(0, 200), new Date().toISOString());
  return Response.json({ id: r.lastInsertRowid }, { status: 201 });
}
