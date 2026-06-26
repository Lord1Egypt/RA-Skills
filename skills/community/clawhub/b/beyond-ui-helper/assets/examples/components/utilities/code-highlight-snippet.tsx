import { CodeHighlight, Card, CardHeader, CardTitle, CardContent, Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

const code = `import { Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function SaveButton() {
  return (
    <Button variant="primary" size="sm">
      Save changes
    </Button>
  );
}`;

export function CodeSnippetPreview() {
  return (
    <Card className="max-w-xl border border-secondary-100">
      <CardHeader>
        <CardTitle>Component implementation</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <CodeHighlight
          language="tsx"
          filename="components/SaveButton.tsx"
          code={code}
          showLineNumbers
        />
        <div className="flex items-center justify-end">
          <Button variant="ghost" size="sm">
            Copy snippet
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
