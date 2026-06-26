package main

import (
	"os"

	"github.com/tencentcloud/cls-cli/cmd"
)

func main() {
	exitCode := cmd.Execute()
	os.Exit(exitCode)
}
