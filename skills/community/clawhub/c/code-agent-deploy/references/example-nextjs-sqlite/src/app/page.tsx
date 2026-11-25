import { getDb } from '@/lib/db';

export const dynamic = 'force-dynamic';

export default function Home() {
  const todos = getDb().prepare('SELECT id, title FROM todos ORDER BY id').all() as { id: number; title: string }[];
  return (
    <main>
      <h1>Todos</h1>
      <p>Address (built in at build time): {process.env.NEXT_PUBLIC_APP_URL ?? 'not set'}</p>
      <p>SQLite version: {(getDb().prepare('select sqlite_version() v').get() as { v: string }).v}</p>
      <ul>{todos.map((t) => <li key={t.id}>{t.title}</li>)}</ul>
    </main>
  );
}
