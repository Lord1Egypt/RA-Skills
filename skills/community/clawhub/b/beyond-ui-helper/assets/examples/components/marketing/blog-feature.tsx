import { Card, CardHeader, CardTitle, CardDescription, CardContent, Badge, Button, Avatar, AvatarImage, AvatarFallback } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { Calendar, ArrowRight, Bookmark } from 'lucide-react';

export function FeaturedBlogPost() {
  return (
    <Card className="flex flex-col overflow-hidden border border-secondary-100 md:flex-row">
      <div className="md:w-1/2">
        <img
          src="https://images.unsplash.com/photo-1506744038136-46273834b3fb"
          alt="Greenhouse"
          className="h-full w-full object-cover"
        />
      </div>
      <div className="flex flex-1 flex-col justify-between p-6">
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Badge variant="info">Case study</Badge>
            <span className="flex items-center gap-1 text-xs text-secondary-500">
              <Calendar className="h-3 w-3" />
              Published Feb 24, 2026
            </span>
          </div>
          <CardHeader className="p-0">
            <CardTitle className="text-2xl">
              How Beyond UI helped Agritech Labs launch dashboards in 3 weeks
            </CardTitle>
            <CardDescription>
              A modular toolkit for shipping production dashboards, landing pages, and secure portals without design debt.
            </CardDescription>
          </CardHeader>
        </div>

        <div className="mt-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar size="sm">
              <AvatarImage src="https://i.pravatar.cc/80?img=12" />
              <AvatarFallback>EL</AvatarFallback>
            </Avatar>
            <div className="text-sm text-secondary-600">
              Eshe Langat
              <div className="text-xs text-secondary-400">Head of Product Marketing</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" aria-label="Save for later">
              <Bookmark className="h-4 w-4" />
            </Button>
            <Button variant="primary" size="sm" className="gap-1">
              Read story
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </Card>
  );
}
