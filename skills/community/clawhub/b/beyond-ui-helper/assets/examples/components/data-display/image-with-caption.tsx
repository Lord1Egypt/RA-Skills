import { Card, CardContent, CardDescription, CardHeader, CardTitle, Image } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function HeroImageCard() {
  return (
    <Card className="overflow-hidden border border-secondary-100">
      <CardHeader className="space-y-1">
        <CardTitle>Crop performance</CardTitle>
        <CardDescription>
          Satellite data captured every 24 hours to monitor vegetation health.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="relative overflow-hidden rounded-xl">
          <Image
            src="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b"
            alt="Aerial view of farmland"
            objectFit="cover"
            height={320}
            width="100%"
            className="w-full"
          />
          <div className="absolute bottom-4 left-4 rounded-md bg-black/60 px-3 py-2 text-xs text-white">
            NDVI Index 0.82 · Updated 3h ago
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
