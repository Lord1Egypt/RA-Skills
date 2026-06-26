#!/bin/bash
# scaffold.sh — Create a new CLI project
# Usage: ./scaffold.sh <name> [--node] [--python] [--go]

set -e

NAME="${1:?Usage: ./scaffold.sh <name> [--node] [--python] [--go]}"
LANG="node"

for arg in "$@"; do
  case $arg in
    --node) LANG="node" ;;
    --python) LANG="python" ;;
    --go) LANG="go" ;;
  esac
done

echo "[cli-builder] Creating $LANG CLI: $NAME"

mkdir -p "$NAME"
cd "$NAME"

case $LANG in
  node)
    mkdir -p src

    cat > package.json << EOF
{
  "name": "$NAME",
  "version": "0.1.0",
  "type": "module",
  "bin": {
    "$NAME": "./dist/cli.js"
  },
  "scripts": {
    "dev": "tsx src/cli.ts",
    "build": "tsup src/cli.ts --format esm --dts",
    "start": "node dist/cli.js",
    "test": "vitest run"
  },
  "dependencies": {
    "commander": "^12.0.0"
  },
  "devDependencies": {
    "tsx": "^4.0.0",
    "tsup": "^8.0.0",
    "typescript": "^5.5.0",
    "vitest": "^2.0.0"
  }
}
EOF

    cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
EOF

    cat > src/cli.ts << EOF
#!/usr/bin/env node
import { Command } from "commander";

const program = new Command();

program
  .name("$NAME")
  .description("$NAME CLI tool")
  .version("0.1.0");

program
  .command("hello")
  .description("Say hello")
  .argument("[name]", "Name to greet", "World")
  .option("-l, --loud", "Use uppercase")
  .action((name: string, opts) => {
    const msg = \`Hello, \${name}!\`;
    console.log(opts.loud ? msg.toUpperCase() : msg);
  });

program.parse();
EOF

    cat > .gitignore << 'EOF'
node_modules/
dist/
EOF

    echo "[OK] Node.js CLI created."
    echo "  cd $NAME && npm install && npm run dev -- hello"
    ;;

  python)
    mkdir -p src tests

    cat > pyproject.toml << EOF
[project]
name = "$NAME"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = ["typer>=0.9.0"]

[project.scripts]
$NAME = "src.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
EOF

    cat > src/__init__.py << 'EOF'
EOF

    cat > src/cli.py << EOF
#!/usr/bin/env python3
"""$NAME CLI tool."""
import typer
from typing_extensions import Annotated
from typing import Optional

app = typer.Typer(name="$NAME", help="$NAME CLI tool")

@app.command()
def hello(
    name: str = typer.Argument("World", help="Name to greet"),
    loud: Annotated[bool, typer.Option("--loud", "-l", help="Use uppercase")] = False,
):
    """Say hello."""
    msg = f"Hello, {name}!"
    typer.echo(msg.upper() if loud else msg)

def version_callback(value: bool):
    if value:
        typer.echo("$NAME v0.1.0")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[Optional[bool], typer.Option("--version", "-v", callback=version_callback, is_eager=True)] = None,
):
    pass

if __name__ == "__main__":
    app()
EOF

    cat > .gitignore << 'EOF'
__pycache__/
*.pyc
dist/
*.egg-info/
venv/
EOF

    echo "[OK] Python CLI created."
    echo "  cd $NAME && pip install -e . && $NAME hello"
    ;;

  go)
    cat > go.mod << EOF
module github.com/user/$NAME

go 1.22

require github.com/spf13/cobra v1.8.0
EOF

    mkdir -p cmd

    cat > cmd/root.go << EOF
package cmd

import (
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"
)

var Version = "0.1.0"

var rootCmd = &cobra.Command{
	Use:   "$NAME",
	Short: "$NAME CLI tool",
}

var helloCmd = &cobra.Command{
	Use:   "hello [name]",
	Short: "Say hello",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		name := "World"
		if len(args) > 0 {
			name = args[0]
		}
		loud, _ := cmd.Flags().GetBool("loud")
		msg := fmt.Sprintf("Hello, %s!", name)
		if loud {
			fmt.Println(strings.ToUpper(msg))
		} else {
			fmt.Println(msg)
		}
	},
}

func init() {
	helloCmd.Flags().BoolP("loud", "l", false, "Use uppercase")
	rootCmd.AddCommand(helloCmd)
	rootCmd.Version = Version
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}
EOF

    cat > main.go << 'EOF'
package main

import "github.com/user/APPNAME/cmd"

func main() {
	cmd.Execute()
}
EOF
    sed -i "s/APPNAME/$NAME/g" main.go

    cat > .gitignore << 'EOF'
bin/
EOF

    echo "[OK] Go CLI created."
    echo "  cd $NAME && go mod tidy && go run . hello"
    ;;
esac
