import { allSettled, fork, serialize } from 'effector';
import { EffectorNext } from '@effector/next';
import { notFound, redirect } from 'next/navigation';
import { PageView } from '@/pages/resource';
import { pageStarted, $notFound, $shouldRedirect } from '@/pages/resource/model/page.model';

export default async function Page({ params }: { params: { id: string } }) {
  const scope = fork();

  await allSettled(pageStarted, {
    scope,
    params: { id: params.id },
  });

  // getState is acceptable here only for Next framework decisions.
  if (scope.getState($notFound)) {
    notFound();
  }

  if (scope.getState($shouldRedirect)) {
    redirect('/login');
  }

  return (
    <EffectorNext values={serialize(scope)}>
      <PageView />
    </EffectorNext>
  );
}
