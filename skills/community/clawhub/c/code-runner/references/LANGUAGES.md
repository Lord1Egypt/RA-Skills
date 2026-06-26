# Supported Languages Reference

This document provides detailed information about each supported programming language, including installation instructions and platform-specific notes.

## Interpreted Languages

### JavaScript
- **Executor**: `node`
- **Extension**: `.js`
- **Install**: [Node.js](https://nodejs.org/)
- **Example**: `console.log('Hello, World!')`

### TypeScript
- **Executor**: `ts-node`
- **Extension**: `.ts`
- **Install**: `npm install -g ts-node typescript`
- **Example**: `console.log('Hello, TypeScript!' as string)`

### Python
- **Executor**: `python -u`
- **Extension**: `.py`
- **Install**: [Python](https://python.org/)
- **Note**: Use `python3` on some systems
- **Example**: `print('Hello, World!')`

### Ruby
- **Executor**: `ruby`
- **Extension**: `.rb`
- **Install**: [Ruby](https://ruby-lang.org/)
- **Example**: `puts 'Hello, World!'`

### PHP
- **Executor**: `php`
- **Extension**: `.php`
- **Install**: [PHP](https://php.net/)
- **Example**: `<?php echo 'Hello, World!'; ?>`

### Perl
- **Executor**: `perl`
- **Extension**: `.pl`
- **Install**: Usually pre-installed on Unix systems
- **Example**: `print "Hello, World!\n";`

### Lua
- **Executor**: `lua`
- **Extension**: `.lua`
- **Install**: [Lua](https://lua.org/)
- **Example**: `print('Hello, World!')`

### R
- **Executor**: `Rscript`
- **Extension**: `.r`
- **Install**: [R](https://r-project.org/)
- **Example**: `print("Hello, World!")`

### Julia
- **Executor**: `julia`
- **Extension**: `.jl`
- **Install**: [Julia](https://julialang.org/)
- **Example**: `println("Hello, World!")`

---

## JVM Languages

### Java
- **Compiler**: `javac`
- **Executor**: `java`
- **Extension**: `.java`
- **Install**: [JDK](https://adoptium.net/)
- **Note**: Class name must match filename
- **Example**:
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### Kotlin (Script)
- **Executor**: `kotlin`
- **Extension**: `.kts`
- **Install**: [Kotlin](https://kotlinlang.org/)
- **Example**: `println("Hello, World!")`

### Scala
- **Executor**: `scala`
- **Extension**: `.scala`
- **Install**: [Scala](https://scala-lang.org/)
- **Example**: `println("Hello, World!")`

### Groovy
- **Executor**: `groovy`
- **Extension**: `.groovy`
- **Install**: [Groovy](https://groovy-lang.org/)
- **Example**: `println 'Hello, World!'`

### Clojure
- **Executor**: `clojure`
- **Extension**: `.clj`
- **Install**: [Clojure](https://clojure.org/)
- **Example**: `(println "Hello, World!")`

---

## Compiled Languages

### C
- **Compiler**: `gcc`
- **Extension**: `.c`
- **Install**: GCC (via build-essential on Linux, Xcode on macOS, MinGW on Windows)
- **Example**:
```c
#include <stdio.h>
int main() {
    printf("Hello, World!\n");
    return 0;
}
```

### C++
- **Compiler**: `g++`
- **Extension**: `.cpp`
- **Install**: Same as C
- **Example**:
```cpp
#include <iostream>
int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

### Go
- **Executor**: `go run`
- **Extension**: `.go`
- **Install**: [Go](https://go.dev/)
- **Example**:
```go
package main
import "fmt"
func main() { fmt.Println("Hello, World!") }
```

### Rust
- **Compiler**: `rustc`
- **Extension**: `.rs`
- **Install**: [Rust](https://rust-lang.org/)
- **Example**:
```rust
fn main() {
    println!("Hello, World!");
}
```

### Swift
- **Executor**: `swift`
- **Extension**: `.swift`
- **Install**: [Swift](https://swift.org/) (pre-installed on macOS)
- **Example**: `print("Hello, World!")`

### Dart
- **Executor**: `dart run`
- **Extension**: `.dart`
- **Install**: [Dart](https://dart.dev/)
- **Example**: `void main() { print('Hello, World!'); }`

### Crystal
- **Executor**: `crystal run`
- **Extension**: `.cr`
- **Install**: [Crystal](https://crystal-lang.org/)
- **Example**: `puts "Hello, World!"`

### Nim
- **Executor**: `nim compile --run`
- **Extension**: `.nim`
- **Install**: [Nim](https://nim-lang.org/)
- **Example**: `echo "Hello, World!"`

---

## Functional Languages

### Haskell
- **Executor**: `runhaskell`
- **Extension**: `.hs`
- **Install**: [GHC](https://haskell.org/ghc/)
- **Example**: `main = putStrLn "Hello, World!"`

### F#
- **Executor**: `dotnet fsi`
- **Extension**: `.fsx`
- **Install**: [.NET SDK](https://dot.net/)
- **Example**: `printfn "Hello, World!"`

### OCaml
- **Executor**: `ocaml`
- **Extension**: `.ml`
- **Install**: [OCaml](https://ocaml.org/)
- **Example**: `print_endline "Hello, World!"`

### Elixir
- **Executor**: `elixir`
- **Extension**: `.exs`
- **Install**: [Elixir](https://elixir-lang.org/)
- **Example**: `IO.puts "Hello, World!"`

### Racket
- **Executor**: `racket`
- **Extension**: `.rkt`
- **Install**: [Racket](https://racket-lang.org/)
- **Example**: `#lang racket\n(displayln "Hello, World!")`

### Scheme
- **Executor**: `scheme --script`
- **Extension**: `.scm`
- **Install**: MIT/GNU Scheme or Chez Scheme
- **Example**: `(display "Hello, World!") (newline)`

### Lisp
- **Executor**: `sbcl --script`
- **Extension**: `.lisp`
- **Install**: [SBCL](http://sbcl.org/)
- **Example**: `(format t "Hello, World!~%")`

---

## Shell/Script Languages

### Bash
- **Executor**: `bash`
- **Extension**: `.sh`
- **Install**: Pre-installed on Unix systems
- **Example**: `echo "Hello, World!"`

### PowerShell
- **Executor**: `pwsh` (cross-platform) or `powershell` (Windows)
- **Extension**: `.ps1`
- **Install**: [PowerShell](https://github.com/PowerShell/PowerShell)
- **Example**: `Write-Host "Hello, World!"`

### Batch (Windows)
- **Executor**: `cmd /c`
- **Extension**: `.bat` or `.cmd`
- **Platform**: Windows only
- **Example**: `@echo Hello, World!`

---

## .NET Languages

### C# Script
- **Executor**: `dotnet script`
- **Extension**: `.csx`
- **Install**: `dotnet tool install -g dotnet-script`
- **Example**: `Console.WriteLine("Hello, World!");`

### VBScript
- **Executor**: `cscript //Nologo`
- **Extension**: `.vbs`
- **Platform**: Windows only
- **Example**: `WScript.Echo "Hello, World!"`

---

## Other Languages

### CoffeeScript
- **Executor**: `coffee`
- **Extension**: `.coffee`
- **Install**: `npm install -g coffeescript`
- **Example**: `console.log 'Hello, World!'`

### AppleScript
- **Executor**: `osascript`
- **Extension**: `.applescript`
- **Platform**: macOS only
- **Example**: `display dialog "Hello, World!"`

### AutoHotkey
- **Executor**: `autohotkey`
- **Extension**: `.ahk`
- **Platform**: Windows only
- **Install**: [AutoHotkey](https://autohotkey.com/)
- **Example**: `MsgBox, Hello, World!`

---

## Language Detection Tips

When the language is not explicitly specified, use these hints:

| Pattern | Language |
|---------|----------|
| `console.log` | JavaScript/TypeScript |
| `print(` with no semicolon | Python |
| `puts` or `def ... end` | Ruby |
| `<?php` | PHP |
| `fmt.Println` or `package main` | Go |
| `fn main()` with `println!` | Rust |
| `public static void main` | Java |
| `#include <` | C/C++ |
| `println(` | Kotlin/Scala |
| `defmodule` | Elixir |
| `IO.puts` | Elixir |
