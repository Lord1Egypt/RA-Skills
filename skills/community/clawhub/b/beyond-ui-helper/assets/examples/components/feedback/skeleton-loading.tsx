import { Skeleton, Card, CardHeader, CardTitle, CardContent } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function AnalyticsSkeleton() {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {[1, 2, 3, 4].map((item) => (
        <Card key={item} className="border border-secondary-100">
          <CardHeader>
            <CardTitle>
              <Skeleton className="h-4 w-32" />
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-10 w-full" />
            <div className="space-y-2">
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-4 w-2/3" />
              <Skeleton className="h-4 w-1/2" />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
