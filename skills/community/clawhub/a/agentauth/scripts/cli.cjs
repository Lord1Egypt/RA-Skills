#!/usr/bin/env node
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// node_modules/commander/lib/error.js
var require_error = __commonJS({
  "node_modules/commander/lib/error.js"(exports2) {
    var CommanderError2 = class extends Error {
      /**
       * Constructs the CommanderError class
       * @param {number} exitCode suggested exit code which could be used with process.exit
       * @param {string} code an id string representing the error
       * @param {string} message human-readable description of the error
       */
      constructor(exitCode, code, message) {
        super(message);
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
        this.code = code;
        this.exitCode = exitCode;
        this.nestedError = void 0;
      }
    };
    var InvalidArgumentError2 = class extends CommanderError2 {
      /**
       * Constructs the InvalidArgumentError class
       * @param {string} [message] explanation of why argument is invalid
       */
      constructor(message) {
        super(1, "commander.invalidArgument", message);
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
      }
    };
    exports2.CommanderError = CommanderError2;
    exports2.InvalidArgumentError = InvalidArgumentError2;
  }
});

// node_modules/commander/lib/argument.js
var require_argument = __commonJS({
  "node_modules/commander/lib/argument.js"(exports2) {
    var { InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var Argument2 = class {
      /**
       * Initialize a new command argument with the given name and description.
       * The default is that the argument is required, and you can explicitly
       * indicate this with <> around the name. Put [] around the name for an optional argument.
       *
       * @param {string} name
       * @param {string} [description]
       */
      constructor(name, description) {
        this.description = description || "";
        this.variadic = false;
        this.parseArg = void 0;
        this.defaultValue = void 0;
        this.defaultValueDescription = void 0;
        this.argChoices = void 0;
        switch (name[0]) {
          case "<":
            this.required = true;
            this._name = name.slice(1, -1);
            break;
          case "[":
            this.required = false;
            this._name = name.slice(1, -1);
            break;
          default:
            this.required = true;
            this._name = name;
            break;
        }
        if (this._name.endsWith("...")) {
          this.variadic = true;
          this._name = this._name.slice(0, -3);
        }
      }
      /**
       * Return argument name.
       *
       * @return {string}
       */
      name() {
        return this._name;
      }
      /**
       * @package
       */
      _collectValue(value, previous) {
        if (previous === this.defaultValue || !Array.isArray(previous)) {
          return [value];
        }
        previous.push(value);
        return previous;
      }
      /**
       * Set the default value, and optionally supply the description to be displayed in the help.
       *
       * @param {*} value
       * @param {string} [description]
       * @return {Argument}
       */
      default(value, description) {
        this.defaultValue = value;
        this.defaultValueDescription = description;
        return this;
      }
      /**
       * Set the custom handler for processing CLI command arguments into argument values.
       *
       * @param {Function} [fn]
       * @return {Argument}
       */
      argParser(fn) {
        this.parseArg = fn;
        return this;
      }
      /**
       * Only allow argument value to be one of choices.
       *
       * @param {string[]} values
       * @return {Argument}
       */
      choices(values) {
        this.argChoices = values.slice();
        this.parseArg = (arg, previous) => {
          if (!this.argChoices.includes(arg)) {
            throw new InvalidArgumentError2(
              `Allowed choices are ${this.argChoices.join(", ")}.`
            );
          }
          if (this.variadic) {
            return this._collectValue(arg, previous);
          }
          return arg;
        };
        return this;
      }
      /**
       * Make argument required.
       *
       * @returns {Argument}
       */
      argRequired() {
        this.required = true;
        return this;
      }
      /**
       * Make argument optional.
       *
       * @returns {Argument}
       */
      argOptional() {
        this.required = false;
        return this;
      }
    };
    function humanReadableArgName(arg) {
      const nameOutput = arg.name() + (arg.variadic === true ? "..." : "");
      return arg.required ? "<" + nameOutput + ">" : "[" + nameOutput + "]";
    }
    exports2.Argument = Argument2;
    exports2.humanReadableArgName = humanReadableArgName;
  }
});

// node_modules/commander/lib/help.js
var require_help = __commonJS({
  "node_modules/commander/lib/help.js"(exports2) {
    var { humanReadableArgName } = require_argument();
    var Help2 = class {
      constructor() {
        this.helpWidth = void 0;
        this.minWidthToWrap = 40;
        this.sortSubcommands = false;
        this.sortOptions = false;
        this.showGlobalOptions = false;
      }
      /**
       * prepareContext is called by Commander after applying overrides from `Command.configureHelp()`
       * and just before calling `formatHelp()`.
       *
       * Commander just uses the helpWidth and the rest is provided for optional use by more complex subclasses.
       *
       * @param {{ error?: boolean, helpWidth?: number, outputHasColors?: boolean }} contextOptions
       */
      prepareContext(contextOptions) {
        this.helpWidth = this.helpWidth ?? contextOptions.helpWidth ?? 80;
      }
      /**
       * Get an array of the visible subcommands. Includes a placeholder for the implicit help command, if there is one.
       *
       * @param {Command} cmd
       * @returns {Command[]}
       */
      visibleCommands(cmd) {
        const visibleCommands = cmd.commands.filter((cmd2) => !cmd2._hidden);
        const helpCommand = cmd._getHelpCommand();
        if (helpCommand && !helpCommand._hidden) {
          visibleCommands.push(helpCommand);
        }
        if (this.sortSubcommands) {
          visibleCommands.sort((a, b) => {
            return a.name().localeCompare(b.name());
          });
        }
        return visibleCommands;
      }
      /**
       * Compare options for sort.
       *
       * @param {Option} a
       * @param {Option} b
       * @returns {number}
       */
      compareOptions(a, b) {
        const getSortKey = (option) => {
          return option.short ? option.short.replace(/^-/, "") : option.long.replace(/^--/, "");
        };
        return getSortKey(a).localeCompare(getSortKey(b));
      }
      /**
       * Get an array of the visible options. Includes a placeholder for the implicit help option, if there is one.
       *
       * @param {Command} cmd
       * @returns {Option[]}
       */
      visibleOptions(cmd) {
        const visibleOptions = cmd.options.filter((option) => !option.hidden);
        const helpOption = cmd._getHelpOption();
        if (helpOption && !helpOption.hidden) {
          const removeShort = helpOption.short && cmd._findOption(helpOption.short);
          const removeLong = helpOption.long && cmd._findOption(helpOption.long);
          if (!removeShort && !removeLong) {
            visibleOptions.push(helpOption);
          } else if (helpOption.long && !removeLong) {
            visibleOptions.push(
              cmd.createOption(helpOption.long, helpOption.description)
            );
          } else if (helpOption.short && !removeShort) {
            visibleOptions.push(
              cmd.createOption(helpOption.short, helpOption.description)
            );
          }
        }
        if (this.sortOptions) {
          visibleOptions.sort(this.compareOptions);
        }
        return visibleOptions;
      }
      /**
       * Get an array of the visible global options. (Not including help.)
       *
       * @param {Command} cmd
       * @returns {Option[]}
       */
      visibleGlobalOptions(cmd) {
        if (!this.showGlobalOptions) return [];
        const globalOptions = [];
        for (let ancestorCmd = cmd.parent; ancestorCmd; ancestorCmd = ancestorCmd.parent) {
          const visibleOptions = ancestorCmd.options.filter(
            (option) => !option.hidden
          );
          globalOptions.push(...visibleOptions);
        }
        if (this.sortOptions) {
          globalOptions.sort(this.compareOptions);
        }
        return globalOptions;
      }
      /**
       * Get an array of the arguments if any have a description.
       *
       * @param {Command} cmd
       * @returns {Argument[]}
       */
      visibleArguments(cmd) {
        if (cmd._argsDescription) {
          cmd.registeredArguments.forEach((argument) => {
            argument.description = argument.description || cmd._argsDescription[argument.name()] || "";
          });
        }
        if (cmd.registeredArguments.find((argument) => argument.description)) {
          return cmd.registeredArguments;
        }
        return [];
      }
      /**
       * Get the command term to show in the list of subcommands.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      subcommandTerm(cmd) {
        const args = cmd.registeredArguments.map((arg) => humanReadableArgName(arg)).join(" ");
        return cmd._name + (cmd._aliases[0] ? "|" + cmd._aliases[0] : "") + (cmd.options.length ? " [options]" : "") + // simplistic check for non-help option
        (args ? " " + args : "");
      }
      /**
       * Get the option term to show in the list of options.
       *
       * @param {Option} option
       * @returns {string}
       */
      optionTerm(option) {
        return option.flags;
      }
      /**
       * Get the argument term to show in the list of arguments.
       *
       * @param {Argument} argument
       * @returns {string}
       */
      argumentTerm(argument) {
        return argument.name();
      }
      /**
       * Get the longest command term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestSubcommandTermLength(cmd, helper) {
        return helper.visibleCommands(cmd).reduce((max, command) => {
          return Math.max(
            max,
            this.displayWidth(
              helper.styleSubcommandTerm(helper.subcommandTerm(command))
            )
          );
        }, 0);
      }
      /**
       * Get the longest option term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestOptionTermLength(cmd, helper) {
        return helper.visibleOptions(cmd).reduce((max, option) => {
          return Math.max(
            max,
            this.displayWidth(helper.styleOptionTerm(helper.optionTerm(option)))
          );
        }, 0);
      }
      /**
       * Get the longest global option term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestGlobalOptionTermLength(cmd, helper) {
        return helper.visibleGlobalOptions(cmd).reduce((max, option) => {
          return Math.max(
            max,
            this.displayWidth(helper.styleOptionTerm(helper.optionTerm(option)))
          );
        }, 0);
      }
      /**
       * Get the longest argument term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestArgumentTermLength(cmd, helper) {
        return helper.visibleArguments(cmd).reduce((max, argument) => {
          return Math.max(
            max,
            this.displayWidth(
              helper.styleArgumentTerm(helper.argumentTerm(argument))
            )
          );
        }, 0);
      }
      /**
       * Get the command usage to be displayed at the top of the built-in help.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      commandUsage(cmd) {
        let cmdName = cmd._name;
        if (cmd._aliases[0]) {
          cmdName = cmdName + "|" + cmd._aliases[0];
        }
        let ancestorCmdNames = "";
        for (let ancestorCmd = cmd.parent; ancestorCmd; ancestorCmd = ancestorCmd.parent) {
          ancestorCmdNames = ancestorCmd.name() + " " + ancestorCmdNames;
        }
        return ancestorCmdNames + cmdName + " " + cmd.usage();
      }
      /**
       * Get the description for the command.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      commandDescription(cmd) {
        return cmd.description();
      }
      /**
       * Get the subcommand summary to show in the list of subcommands.
       * (Fallback to description for backwards compatibility.)
       *
       * @param {Command} cmd
       * @returns {string}
       */
      subcommandDescription(cmd) {
        return cmd.summary() || cmd.description();
      }
      /**
       * Get the option description to show in the list of options.
       *
       * @param {Option} option
       * @return {string}
       */
      optionDescription(option) {
        const extraInfo = [];
        if (option.argChoices) {
          extraInfo.push(
            // use stringify to match the display of the default value
            `choices: ${option.argChoices.map((choice) => JSON.stringify(choice)).join(", ")}`
          );
        }
        if (option.defaultValue !== void 0) {
          const showDefault = option.required || option.optional || option.isBoolean() && typeof option.defaultValue === "boolean";
          if (showDefault) {
            extraInfo.push(
              `default: ${option.defaultValueDescription || JSON.stringify(option.defaultValue)}`
            );
          }
        }
        if (option.presetArg !== void 0 && option.optional) {
          extraInfo.push(`preset: ${JSON.stringify(option.presetArg)}`);
        }
        if (option.envVar !== void 0) {
          extraInfo.push(`env: ${option.envVar}`);
        }
        if (extraInfo.length > 0) {
          const extraDescription = `(${extraInfo.join(", ")})`;
          if (option.description) {
            return `${option.description} ${extraDescription}`;
          }
          return extraDescription;
        }
        return option.description;
      }
      /**
       * Get the argument description to show in the list of arguments.
       *
       * @param {Argument} argument
       * @return {string}
       */
      argumentDescription(argument) {
        const extraInfo = [];
        if (argument.argChoices) {
          extraInfo.push(
            // use stringify to match the display of the default value
            `choices: ${argument.argChoices.map((choice) => JSON.stringify(choice)).join(", ")}`
          );
        }
        if (argument.defaultValue !== void 0) {
          extraInfo.push(
            `default: ${argument.defaultValueDescription || JSON.stringify(argument.defaultValue)}`
          );
        }
        if (extraInfo.length > 0) {
          const extraDescription = `(${extraInfo.join(", ")})`;
          if (argument.description) {
            return `${argument.description} ${extraDescription}`;
          }
          return extraDescription;
        }
        return argument.description;
      }
      /**
       * Format a list of items, given a heading and an array of formatted items.
       *
       * @param {string} heading
       * @param {string[]} items
       * @param {Help} helper
       * @returns string[]
       */
      formatItemList(heading, items, helper) {
        if (items.length === 0) return [];
        return [helper.styleTitle(heading), ...items, ""];
      }
      /**
       * Group items by their help group heading.
       *
       * @param {Command[] | Option[]} unsortedItems
       * @param {Command[] | Option[]} visibleItems
       * @param {Function} getGroup
       * @returns {Map<string, Command[] | Option[]>}
       */
      groupItems(unsortedItems, visibleItems, getGroup) {
        const result = /* @__PURE__ */ new Map();
        unsortedItems.forEach((item) => {
          const group = getGroup(item);
          if (!result.has(group)) result.set(group, []);
        });
        visibleItems.forEach((item) => {
          const group = getGroup(item);
          if (!result.has(group)) {
            result.set(group, []);
          }
          result.get(group).push(item);
        });
        return result;
      }
      /**
       * Generate the built-in help text.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {string}
       */
      formatHelp(cmd, helper) {
        const termWidth = helper.padWidth(cmd, helper);
        const helpWidth = helper.helpWidth ?? 80;
        function callFormatItem(term, description) {
          return helper.formatItem(term, termWidth, description, helper);
        }
        let output = [
          `${helper.styleTitle("Usage:")} ${helper.styleUsage(helper.commandUsage(cmd))}`,
          ""
        ];
        const commandDescription = helper.commandDescription(cmd);
        if (commandDescription.length > 0) {
          output = output.concat([
            helper.boxWrap(
              helper.styleCommandDescription(commandDescription),
              helpWidth
            ),
            ""
          ]);
        }
        const argumentList = helper.visibleArguments(cmd).map((argument) => {
          return callFormatItem(
            helper.styleArgumentTerm(helper.argumentTerm(argument)),
            helper.styleArgumentDescription(helper.argumentDescription(argument))
          );
        });
        output = output.concat(
          this.formatItemList("Arguments:", argumentList, helper)
        );
        const optionGroups = this.groupItems(
          cmd.options,
          helper.visibleOptions(cmd),
          (option) => option.helpGroupHeading ?? "Options:"
        );
        optionGroups.forEach((options, group) => {
          const optionList = options.map((option) => {
            return callFormatItem(
              helper.styleOptionTerm(helper.optionTerm(option)),
              helper.styleOptionDescription(helper.optionDescription(option))
            );
          });
          output = output.concat(this.formatItemList(group, optionList, helper));
        });
        if (helper.showGlobalOptions) {
          const globalOptionList = helper.visibleGlobalOptions(cmd).map((option) => {
            return callFormatItem(
              helper.styleOptionTerm(helper.optionTerm(option)),
              helper.styleOptionDescription(helper.optionDescription(option))
            );
          });
          output = output.concat(
            this.formatItemList("Global Options:", globalOptionList, helper)
          );
        }
        const commandGroups = this.groupItems(
          cmd.commands,
          helper.visibleCommands(cmd),
          (sub) => sub.helpGroup() || "Commands:"
        );
        commandGroups.forEach((commands, group) => {
          const commandList = commands.map((sub) => {
            return callFormatItem(
              helper.styleSubcommandTerm(helper.subcommandTerm(sub)),
              helper.styleSubcommandDescription(helper.subcommandDescription(sub))
            );
          });
          output = output.concat(this.formatItemList(group, commandList, helper));
        });
        return output.join("\n");
      }
      /**
       * Return display width of string, ignoring ANSI escape sequences. Used in padding and wrapping calculations.
       *
       * @param {string} str
       * @returns {number}
       */
      displayWidth(str) {
        return stripColor(str).length;
      }
      /**
       * Style the title for displaying in the help. Called with 'Usage:', 'Options:', etc.
       *
       * @param {string} str
       * @returns {string}
       */
      styleTitle(str) {
        return str;
      }
      styleUsage(str) {
        return str.split(" ").map((word) => {
          if (word === "[options]") return this.styleOptionText(word);
          if (word === "[command]") return this.styleSubcommandText(word);
          if (word[0] === "[" || word[0] === "<")
            return this.styleArgumentText(word);
          return this.styleCommandText(word);
        }).join(" ");
      }
      styleCommandDescription(str) {
        return this.styleDescriptionText(str);
      }
      styleOptionDescription(str) {
        return this.styleDescriptionText(str);
      }
      styleSubcommandDescription(str) {
        return this.styleDescriptionText(str);
      }
      styleArgumentDescription(str) {
        return this.styleDescriptionText(str);
      }
      styleDescriptionText(str) {
        return str;
      }
      styleOptionTerm(str) {
        return this.styleOptionText(str);
      }
      styleSubcommandTerm(str) {
        return str.split(" ").map((word) => {
          if (word === "[options]") return this.styleOptionText(word);
          if (word[0] === "[" || word[0] === "<")
            return this.styleArgumentText(word);
          return this.styleSubcommandText(word);
        }).join(" ");
      }
      styleArgumentTerm(str) {
        return this.styleArgumentText(str);
      }
      styleOptionText(str) {
        return str;
      }
      styleArgumentText(str) {
        return str;
      }
      styleSubcommandText(str) {
        return str;
      }
      styleCommandText(str) {
        return str;
      }
      /**
       * Calculate the pad width from the maximum term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      padWidth(cmd, helper) {
        return Math.max(
          helper.longestOptionTermLength(cmd, helper),
          helper.longestGlobalOptionTermLength(cmd, helper),
          helper.longestSubcommandTermLength(cmd, helper),
          helper.longestArgumentTermLength(cmd, helper)
        );
      }
      /**
       * Detect manually wrapped and indented strings by checking for line break followed by whitespace.
       *
       * @param {string} str
       * @returns {boolean}
       */
      preformatted(str) {
        return /\n[^\S\r\n]/.test(str);
      }
      /**
       * Format the "item", which consists of a term and description. Pad the term and wrap the description, indenting the following lines.
       *
       * So "TTT", 5, "DDD DDDD DD DDD" might be formatted for this.helpWidth=17 like so:
       *   TTT  DDD DDDD
       *        DD DDD
       *
       * @param {string} term
       * @param {number} termWidth
       * @param {string} description
       * @param {Help} helper
       * @returns {string}
       */
      formatItem(term, termWidth, description, helper) {
        const itemIndent = 2;
        const itemIndentStr = " ".repeat(itemIndent);
        if (!description) return itemIndentStr + term;
        const paddedTerm = term.padEnd(
          termWidth + term.length - helper.displayWidth(term)
        );
        const spacerWidth = 2;
        const helpWidth = this.helpWidth ?? 80;
        const remainingWidth = helpWidth - termWidth - spacerWidth - itemIndent;
        let formattedDescription;
        if (remainingWidth < this.minWidthToWrap || helper.preformatted(description)) {
          formattedDescription = description;
        } else {
          const wrappedDescription = helper.boxWrap(description, remainingWidth);
          formattedDescription = wrappedDescription.replace(
            /\n/g,
            "\n" + " ".repeat(termWidth + spacerWidth)
          );
        }
        return itemIndentStr + paddedTerm + " ".repeat(spacerWidth) + formattedDescription.replace(/\n/g, `
${itemIndentStr}`);
      }
      /**
       * Wrap a string at whitespace, preserving existing line breaks.
       * Wrapping is skipped if the width is less than `minWidthToWrap`.
       *
       * @param {string} str
       * @param {number} width
       * @returns {string}
       */
      boxWrap(str, width) {
        if (width < this.minWidthToWrap) return str;
        const rawLines = str.split(/\r\n|\n/);
        const chunkPattern = /[\s]*[^\s]+/g;
        const wrappedLines = [];
        rawLines.forEach((line) => {
          const chunks = line.match(chunkPattern);
          if (chunks === null) {
            wrappedLines.push("");
            return;
          }
          let sumChunks = [chunks.shift()];
          let sumWidth = this.displayWidth(sumChunks[0]);
          chunks.forEach((chunk) => {
            const visibleWidth = this.displayWidth(chunk);
            if (sumWidth + visibleWidth <= width) {
              sumChunks.push(chunk);
              sumWidth += visibleWidth;
              return;
            }
            wrappedLines.push(sumChunks.join(""));
            const nextChunk = chunk.trimStart();
            sumChunks = [nextChunk];
            sumWidth = this.displayWidth(nextChunk);
          });
          wrappedLines.push(sumChunks.join(""));
        });
        return wrappedLines.join("\n");
      }
    };
    function stripColor(str) {
      const sgrPattern = /\x1b\[\d*(;\d*)*m/g;
      return str.replace(sgrPattern, "");
    }
    exports2.Help = Help2;
    exports2.stripColor = stripColor;
  }
});

// node_modules/commander/lib/option.js
var require_option = __commonJS({
  "node_modules/commander/lib/option.js"(exports2) {
    var { InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var Option2 = class {
      /**
       * Initialize a new `Option` with the given `flags` and `description`.
       *
       * @param {string} flags
       * @param {string} [description]
       */
      constructor(flags, description) {
        this.flags = flags;
        this.description = description || "";
        this.required = flags.includes("<");
        this.optional = flags.includes("[");
        this.variadic = /\w\.\.\.[>\]]$/.test(flags);
        this.mandatory = false;
        const optionFlags = splitOptionFlags(flags);
        this.short = optionFlags.shortFlag;
        this.long = optionFlags.longFlag;
        this.negate = false;
        if (this.long) {
          this.negate = this.long.startsWith("--no-");
        }
        this.defaultValue = void 0;
        this.defaultValueDescription = void 0;
        this.presetArg = void 0;
        this.envVar = void 0;
        this.parseArg = void 0;
        this.hidden = false;
        this.argChoices = void 0;
        this.conflictsWith = [];
        this.implied = void 0;
        this.helpGroupHeading = void 0;
      }
      /**
       * Set the default value, and optionally supply the description to be displayed in the help.
       *
       * @param {*} value
       * @param {string} [description]
       * @return {Option}
       */
      default(value, description) {
        this.defaultValue = value;
        this.defaultValueDescription = description;
        return this;
      }
      /**
       * Preset to use when option used without option-argument, especially optional but also boolean and negated.
       * The custom processing (parseArg) is called.
       *
       * @example
       * new Option('--color').default('GREYSCALE').preset('RGB');
       * new Option('--donate [amount]').preset('20').argParser(parseFloat);
       *
       * @param {*} arg
       * @return {Option}
       */
      preset(arg) {
        this.presetArg = arg;
        return this;
      }
      /**
       * Add option name(s) that conflict with this option.
       * An error will be displayed if conflicting options are found during parsing.
       *
       * @example
       * new Option('--rgb').conflicts('cmyk');
       * new Option('--js').conflicts(['ts', 'jsx']);
       *
       * @param {(string | string[])} names
       * @return {Option}
       */
      conflicts(names) {
        this.conflictsWith = this.conflictsWith.concat(names);
        return this;
      }
      /**
       * Specify implied option values for when this option is set and the implied options are not.
       *
       * The custom processing (parseArg) is not called on the implied values.
       *
       * @example
       * program
       *   .addOption(new Option('--log', 'write logging information to file'))
       *   .addOption(new Option('--trace', 'log extra details').implies({ log: 'trace.txt' }));
       *
       * @param {object} impliedOptionValues
       * @return {Option}
       */
      implies(impliedOptionValues) {
        let newImplied = impliedOptionValues;
        if (typeof impliedOptionValues === "string") {
          newImplied = { [impliedOptionValues]: true };
        }
        this.implied = Object.assign(this.implied || {}, newImplied);
        return this;
      }
      /**
       * Set environment variable to check for option value.
       *
       * An environment variable is only used if when processed the current option value is
       * undefined, or the source of the current value is 'default' or 'config' or 'env'.
       *
       * @param {string} name
       * @return {Option}
       */
      env(name) {
        this.envVar = name;
        return this;
      }
      /**
       * Set the custom handler for processing CLI option arguments into option values.
       *
       * @param {Function} [fn]
       * @return {Option}
       */
      argParser(fn) {
        this.parseArg = fn;
        return this;
      }
      /**
       * Whether the option is mandatory and must have a value after parsing.
       *
       * @param {boolean} [mandatory=true]
       * @return {Option}
       */
      makeOptionMandatory(mandatory = true) {
        this.mandatory = !!mandatory;
        return this;
      }
      /**
       * Hide option in help.
       *
       * @param {boolean} [hide=true]
       * @return {Option}
       */
      hideHelp(hide = true) {
        this.hidden = !!hide;
        return this;
      }
      /**
       * @package
       */
      _collectValue(value, previous) {
        if (previous === this.defaultValue || !Array.isArray(previous)) {
          return [value];
        }
        previous.push(value);
        return previous;
      }
      /**
       * Only allow option value to be one of choices.
       *
       * @param {string[]} values
       * @return {Option}
       */
      choices(values) {
        this.argChoices = values.slice();
        this.parseArg = (arg, previous) => {
          if (!this.argChoices.includes(arg)) {
            throw new InvalidArgumentError2(
              `Allowed choices are ${this.argChoices.join(", ")}.`
            );
          }
          if (this.variadic) {
            return this._collectValue(arg, previous);
          }
          return arg;
        };
        return this;
      }
      /**
       * Return option name.
       *
       * @return {string}
       */
      name() {
        if (this.long) {
          return this.long.replace(/^--/, "");
        }
        return this.short.replace(/^-/, "");
      }
      /**
       * Return option name, in a camelcase format that can be used
       * as an object attribute key.
       *
       * @return {string}
       */
      attributeName() {
        if (this.negate) {
          return camelcase(this.name().replace(/^no-/, ""));
        }
        return camelcase(this.name());
      }
      /**
       * Set the help group heading.
       *
       * @param {string} heading
       * @return {Option}
       */
      helpGroup(heading) {
        this.helpGroupHeading = heading;
        return this;
      }
      /**
       * Check if `arg` matches the short or long flag.
       *
       * @param {string} arg
       * @return {boolean}
       * @package
       */
      is(arg) {
        return this.short === arg || this.long === arg;
      }
      /**
       * Return whether a boolean option.
       *
       * Options are one of boolean, negated, required argument, or optional argument.
       *
       * @return {boolean}
       * @package
       */
      isBoolean() {
        return !this.required && !this.optional && !this.negate;
      }
    };
    var DualOptions = class {
      /**
       * @param {Option[]} options
       */
      constructor(options) {
        this.positiveOptions = /* @__PURE__ */ new Map();
        this.negativeOptions = /* @__PURE__ */ new Map();
        this.dualOptions = /* @__PURE__ */ new Set();
        options.forEach((option) => {
          if (option.negate) {
            this.negativeOptions.set(option.attributeName(), option);
          } else {
            this.positiveOptions.set(option.attributeName(), option);
          }
        });
        this.negativeOptions.forEach((value, key) => {
          if (this.positiveOptions.has(key)) {
            this.dualOptions.add(key);
          }
        });
      }
      /**
       * Did the value come from the option, and not from possible matching dual option?
       *
       * @param {*} value
       * @param {Option} option
       * @returns {boolean}
       */
      valueFromOption(value, option) {
        const optionKey = option.attributeName();
        if (!this.dualOptions.has(optionKey)) return true;
        const preset = this.negativeOptions.get(optionKey).presetArg;
        const negativeValue = preset !== void 0 ? preset : false;
        return option.negate === (negativeValue === value);
      }
    };
    function camelcase(str) {
      return str.split("-").reduce((str2, word) => {
        return str2 + word[0].toUpperCase() + word.slice(1);
      });
    }
    function splitOptionFlags(flags) {
      let shortFlag;
      let longFlag;
      const shortFlagExp = /^-[^-]$/;
      const longFlagExp = /^--[^-]/;
      const flagParts = flags.split(/[ |,]+/).concat("guard");
      if (shortFlagExp.test(flagParts[0])) shortFlag = flagParts.shift();
      if (longFlagExp.test(flagParts[0])) longFlag = flagParts.shift();
      if (!shortFlag && shortFlagExp.test(flagParts[0]))
        shortFlag = flagParts.shift();
      if (!shortFlag && longFlagExp.test(flagParts[0])) {
        shortFlag = longFlag;
        longFlag = flagParts.shift();
      }
      if (flagParts[0].startsWith("-")) {
        const unsupportedFlag = flagParts[0];
        const baseError = `option creation failed due to '${unsupportedFlag}' in option flags '${flags}'`;
        if (/^-[^-][^-]/.test(unsupportedFlag))
          throw new Error(
            `${baseError}
- a short flag is a single dash and a single character
  - either use a single dash and a single character (for a short flag)
  - or use a double dash for a long option (and can have two, like '--ws, --workspace')`
          );
        if (shortFlagExp.test(unsupportedFlag))
          throw new Error(`${baseError}
- too many short flags`);
        if (longFlagExp.test(unsupportedFlag))
          throw new Error(`${baseError}
- too many long flags`);
        throw new Error(`${baseError}
- unrecognised flag format`);
      }
      if (shortFlag === void 0 && longFlag === void 0)
        throw new Error(
          `option creation failed due to no flags found in '${flags}'.`
        );
      return { shortFlag, longFlag };
    }
    exports2.Option = Option2;
    exports2.DualOptions = DualOptions;
  }
});

// node_modules/commander/lib/suggestSimilar.js
var require_suggestSimilar = __commonJS({
  "node_modules/commander/lib/suggestSimilar.js"(exports2) {
    var maxDistance = 3;
    function editDistance(a, b) {
      if (Math.abs(a.length - b.length) > maxDistance)
        return Math.max(a.length, b.length);
      const d = [];
      for (let i = 0; i <= a.length; i++) {
        d[i] = [i];
      }
      for (let j = 0; j <= b.length; j++) {
        d[0][j] = j;
      }
      for (let j = 1; j <= b.length; j++) {
        for (let i = 1; i <= a.length; i++) {
          let cost = 1;
          if (a[i - 1] === b[j - 1]) {
            cost = 0;
          } else {
            cost = 1;
          }
          d[i][j] = Math.min(
            d[i - 1][j] + 1,
            // deletion
            d[i][j - 1] + 1,
            // insertion
            d[i - 1][j - 1] + cost
            // substitution
          );
          if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
            d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
          }
        }
      }
      return d[a.length][b.length];
    }
    function suggestSimilar(word, candidates) {
      if (!candidates || candidates.length === 0) return "";
      candidates = Array.from(new Set(candidates));
      const searchingOptions = word.startsWith("--");
      if (searchingOptions) {
        word = word.slice(2);
        candidates = candidates.map((candidate) => candidate.slice(2));
      }
      let similar = [];
      let bestDistance = maxDistance;
      const minSimilarity = 0.4;
      candidates.forEach((candidate) => {
        if (candidate.length <= 1) return;
        const distance = editDistance(word, candidate);
        const length = Math.max(word.length, candidate.length);
        const similarity = (length - distance) / length;
        if (similarity > minSimilarity) {
          if (distance < bestDistance) {
            bestDistance = distance;
            similar = [candidate];
          } else if (distance === bestDistance) {
            similar.push(candidate);
          }
        }
      });
      similar.sort((a, b) => a.localeCompare(b));
      if (searchingOptions) {
        similar = similar.map((candidate) => `--${candidate}`);
      }
      if (similar.length > 1) {
        return `
(Did you mean one of ${similar.join(", ")}?)`;
      }
      if (similar.length === 1) {
        return `
(Did you mean ${similar[0]}?)`;
      }
      return "";
    }
    exports2.suggestSimilar = suggestSimilar;
  }
});

// node_modules/commander/lib/command.js
var require_command = __commonJS({
  "node_modules/commander/lib/command.js"(exports2) {
    var EventEmitter = require("node:events").EventEmitter;
    var childProcess4 = require("node:child_process");
    var path5 = require("node:path");
    var fs7 = require("node:fs");
    var process9 = require("node:process");
    var { Argument: Argument2, humanReadableArgName } = require_argument();
    var { CommanderError: CommanderError2 } = require_error();
    var { Help: Help2, stripColor } = require_help();
    var { Option: Option2, DualOptions } = require_option();
    var { suggestSimilar } = require_suggestSimilar();
    var Command2 = class _Command extends EventEmitter {
      /**
       * Initialize a new `Command`.
       *
       * @param {string} [name]
       */
      constructor(name) {
        super();
        this.commands = [];
        this.options = [];
        this.parent = null;
        this._allowUnknownOption = false;
        this._allowExcessArguments = false;
        this.registeredArguments = [];
        this._args = this.registeredArguments;
        this.args = [];
        this.rawArgs = [];
        this.processedArgs = [];
        this._scriptPath = null;
        this._name = name || "";
        this._optionValues = {};
        this._optionValueSources = {};
        this._storeOptionsAsProperties = false;
        this._actionHandler = null;
        this._executableHandler = false;
        this._executableFile = null;
        this._executableDir = null;
        this._defaultCommandName = null;
        this._exitCallback = null;
        this._aliases = [];
        this._combineFlagAndOptionalValue = true;
        this._description = "";
        this._summary = "";
        this._argsDescription = void 0;
        this._enablePositionalOptions = false;
        this._passThroughOptions = false;
        this._lifeCycleHooks = {};
        this._showHelpAfterError = false;
        this._showSuggestionAfterError = true;
        this._savedState = null;
        this._outputConfiguration = {
          writeOut: (str) => process9.stdout.write(str),
          writeErr: (str) => process9.stderr.write(str),
          outputError: (str, write) => write(str),
          getOutHelpWidth: () => process9.stdout.isTTY ? process9.stdout.columns : void 0,
          getErrHelpWidth: () => process9.stderr.isTTY ? process9.stderr.columns : void 0,
          getOutHasColors: () => useColor() ?? (process9.stdout.isTTY && process9.stdout.hasColors?.()),
          getErrHasColors: () => useColor() ?? (process9.stderr.isTTY && process9.stderr.hasColors?.()),
          stripColor: (str) => stripColor(str)
        };
        this._hidden = false;
        this._helpOption = void 0;
        this._addImplicitHelpCommand = void 0;
        this._helpCommand = void 0;
        this._helpConfiguration = {};
        this._helpGroupHeading = void 0;
        this._defaultCommandGroup = void 0;
        this._defaultOptionGroup = void 0;
      }
      /**
       * Copy settings that are useful to have in common across root command and subcommands.
       *
       * (Used internally when adding a command using `.command()` so subcommands inherit parent settings.)
       *
       * @param {Command} sourceCommand
       * @return {Command} `this` command for chaining
       */
      copyInheritedSettings(sourceCommand) {
        this._outputConfiguration = sourceCommand._outputConfiguration;
        this._helpOption = sourceCommand._helpOption;
        this._helpCommand = sourceCommand._helpCommand;
        this._helpConfiguration = sourceCommand._helpConfiguration;
        this._exitCallback = sourceCommand._exitCallback;
        this._storeOptionsAsProperties = sourceCommand._storeOptionsAsProperties;
        this._combineFlagAndOptionalValue = sourceCommand._combineFlagAndOptionalValue;
        this._allowExcessArguments = sourceCommand._allowExcessArguments;
        this._enablePositionalOptions = sourceCommand._enablePositionalOptions;
        this._showHelpAfterError = sourceCommand._showHelpAfterError;
        this._showSuggestionAfterError = sourceCommand._showSuggestionAfterError;
        return this;
      }
      /**
       * @returns {Command[]}
       * @private
       */
      _getCommandAndAncestors() {
        const result = [];
        for (let command = this; command; command = command.parent) {
          result.push(command);
        }
        return result;
      }
      /**
       * Define a command.
       *
       * There are two styles of command: pay attention to where to put the description.
       *
       * @example
       * // Command implemented using action handler (description is supplied separately to `.command`)
       * program
       *   .command('clone <source> [destination]')
       *   .description('clone a repository into a newly created directory')
       *   .action((source, destination) => {
       *     console.log('clone command called');
       *   });
       *
       * // Command implemented using separate executable file (description is second parameter to `.command`)
       * program
       *   .command('start <service>', 'start named service')
       *   .command('stop [service]', 'stop named service, or all if no name supplied');
       *
       * @param {string} nameAndArgs - command name and arguments, args are `<required>` or `[optional]` and last may also be `variadic...`
       * @param {(object | string)} [actionOptsOrExecDesc] - configuration options (for action), or description (for executable)
       * @param {object} [execOpts] - configuration options (for executable)
       * @return {Command} returns new command for action handler, or `this` for executable command
       */
      command(nameAndArgs, actionOptsOrExecDesc, execOpts) {
        let desc = actionOptsOrExecDesc;
        let opts = execOpts;
        if (typeof desc === "object" && desc !== null) {
          opts = desc;
          desc = null;
        }
        opts = opts || {};
        const [, name, args] = nameAndArgs.match(/([^ ]+) *(.*)/);
        const cmd = this.createCommand(name);
        if (desc) {
          cmd.description(desc);
          cmd._executableHandler = true;
        }
        if (opts.isDefault) this._defaultCommandName = cmd._name;
        cmd._hidden = !!(opts.noHelp || opts.hidden);
        cmd._executableFile = opts.executableFile || null;
        if (args) cmd.arguments(args);
        this._registerCommand(cmd);
        cmd.parent = this;
        cmd.copyInheritedSettings(this);
        if (desc) return this;
        return cmd;
      }
      /**
       * Factory routine to create a new unattached command.
       *
       * See .command() for creating an attached subcommand, which uses this routine to
       * create the command. You can override createCommand to customise subcommands.
       *
       * @param {string} [name]
       * @return {Command} new command
       */
      createCommand(name) {
        return new _Command(name);
      }
      /**
       * You can customise the help with a subclass of Help by overriding createHelp,
       * or by overriding Help properties using configureHelp().
       *
       * @return {Help}
       */
      createHelp() {
        return Object.assign(new Help2(), this.configureHelp());
      }
      /**
       * You can customise the help by overriding Help properties using configureHelp(),
       * or with a subclass of Help by overriding createHelp().
       *
       * @param {object} [configuration] - configuration options
       * @return {(Command | object)} `this` command for chaining, or stored configuration
       */
      configureHelp(configuration) {
        if (configuration === void 0) return this._helpConfiguration;
        this._helpConfiguration = configuration;
        return this;
      }
      /**
       * The default output goes to stdout and stderr. You can customise this for special
       * applications. You can also customise the display of errors by overriding outputError.
       *
       * The configuration properties are all functions:
       *
       *     // change how output being written, defaults to stdout and stderr
       *     writeOut(str)
       *     writeErr(str)
       *     // change how output being written for errors, defaults to writeErr
       *     outputError(str, write) // used for displaying errors and not used for displaying help
       *     // specify width for wrapping help
       *     getOutHelpWidth()
       *     getErrHelpWidth()
       *     // color support, currently only used with Help
       *     getOutHasColors()
       *     getErrHasColors()
       *     stripColor() // used to remove ANSI escape codes if output does not have colors
       *
       * @param {object} [configuration] - configuration options
       * @return {(Command | object)} `this` command for chaining, or stored configuration
       */
      configureOutput(configuration) {
        if (configuration === void 0) return this._outputConfiguration;
        this._outputConfiguration = {
          ...this._outputConfiguration,
          ...configuration
        };
        return this;
      }
      /**
       * Display the help or a custom message after an error occurs.
       *
       * @param {(boolean|string)} [displayHelp]
       * @return {Command} `this` command for chaining
       */
      showHelpAfterError(displayHelp = true) {
        if (typeof displayHelp !== "string") displayHelp = !!displayHelp;
        this._showHelpAfterError = displayHelp;
        return this;
      }
      /**
       * Display suggestion of similar commands for unknown commands, or options for unknown options.
       *
       * @param {boolean} [displaySuggestion]
       * @return {Command} `this` command for chaining
       */
      showSuggestionAfterError(displaySuggestion = true) {
        this._showSuggestionAfterError = !!displaySuggestion;
        return this;
      }
      /**
       * Add a prepared subcommand.
       *
       * See .command() for creating an attached subcommand which inherits settings from its parent.
       *
       * @param {Command} cmd - new subcommand
       * @param {object} [opts] - configuration options
       * @return {Command} `this` command for chaining
       */
      addCommand(cmd, opts) {
        if (!cmd._name) {
          throw new Error(`Command passed to .addCommand() must have a name
- specify the name in Command constructor or using .name()`);
        }
        opts = opts || {};
        if (opts.isDefault) this._defaultCommandName = cmd._name;
        if (opts.noHelp || opts.hidden) cmd._hidden = true;
        this._registerCommand(cmd);
        cmd.parent = this;
        cmd._checkForBrokenPassThrough();
        return this;
      }
      /**
       * Factory routine to create a new unattached argument.
       *
       * See .argument() for creating an attached argument, which uses this routine to
       * create the argument. You can override createArgument to return a custom argument.
       *
       * @param {string} name
       * @param {string} [description]
       * @return {Argument} new argument
       */
      createArgument(name, description) {
        return new Argument2(name, description);
      }
      /**
       * Define argument syntax for command.
       *
       * The default is that the argument is required, and you can explicitly
       * indicate this with <> around the name. Put [] around the name for an optional argument.
       *
       * @example
       * program.argument('<input-file>');
       * program.argument('[output-file]');
       *
       * @param {string} name
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom argument processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      argument(name, description, parseArg, defaultValue) {
        const argument = this.createArgument(name, description);
        if (typeof parseArg === "function") {
          argument.default(defaultValue).argParser(parseArg);
        } else {
          argument.default(parseArg);
        }
        this.addArgument(argument);
        return this;
      }
      /**
       * Define argument syntax for command, adding multiple at once (without descriptions).
       *
       * See also .argument().
       *
       * @example
       * program.arguments('<cmd> [env]');
       *
       * @param {string} names
       * @return {Command} `this` command for chaining
       */
      arguments(names) {
        names.trim().split(/ +/).forEach((detail) => {
          this.argument(detail);
        });
        return this;
      }
      /**
       * Define argument syntax for command, adding a prepared argument.
       *
       * @param {Argument} argument
       * @return {Command} `this` command for chaining
       */
      addArgument(argument) {
        const previousArgument = this.registeredArguments.slice(-1)[0];
        if (previousArgument?.variadic) {
          throw new Error(
            `only the last argument can be variadic '${previousArgument.name()}'`
          );
        }
        if (argument.required && argument.defaultValue !== void 0 && argument.parseArg === void 0) {
          throw new Error(
            `a default value for a required argument is never used: '${argument.name()}'`
          );
        }
        this.registeredArguments.push(argument);
        return this;
      }
      /**
       * Customise or override default help command. By default a help command is automatically added if your command has subcommands.
       *
       * @example
       *    program.helpCommand('help [cmd]');
       *    program.helpCommand('help [cmd]', 'show help');
       *    program.helpCommand(false); // suppress default help command
       *    program.helpCommand(true); // add help command even if no subcommands
       *
       * @param {string|boolean} enableOrNameAndArgs - enable with custom name and/or arguments, or boolean to override whether added
       * @param {string} [description] - custom description
       * @return {Command} `this` command for chaining
       */
      helpCommand(enableOrNameAndArgs, description) {
        if (typeof enableOrNameAndArgs === "boolean") {
          this._addImplicitHelpCommand = enableOrNameAndArgs;
          if (enableOrNameAndArgs && this._defaultCommandGroup) {
            this._initCommandGroup(this._getHelpCommand());
          }
          return this;
        }
        const nameAndArgs = enableOrNameAndArgs ?? "help [command]";
        const [, helpName, helpArgs] = nameAndArgs.match(/([^ ]+) *(.*)/);
        const helpDescription = description ?? "display help for command";
        const helpCommand = this.createCommand(helpName);
        helpCommand.helpOption(false);
        if (helpArgs) helpCommand.arguments(helpArgs);
        if (helpDescription) helpCommand.description(helpDescription);
        this._addImplicitHelpCommand = true;
        this._helpCommand = helpCommand;
        if (enableOrNameAndArgs || description) this._initCommandGroup(helpCommand);
        return this;
      }
      /**
       * Add prepared custom help command.
       *
       * @param {(Command|string|boolean)} helpCommand - custom help command, or deprecated enableOrNameAndArgs as for `.helpCommand()`
       * @param {string} [deprecatedDescription] - deprecated custom description used with custom name only
       * @return {Command} `this` command for chaining
       */
      addHelpCommand(helpCommand, deprecatedDescription) {
        if (typeof helpCommand !== "object") {
          this.helpCommand(helpCommand, deprecatedDescription);
          return this;
        }
        this._addImplicitHelpCommand = true;
        this._helpCommand = helpCommand;
        this._initCommandGroup(helpCommand);
        return this;
      }
      /**
       * Lazy create help command.
       *
       * @return {(Command|null)}
       * @package
       */
      _getHelpCommand() {
        const hasImplicitHelpCommand = this._addImplicitHelpCommand ?? (this.commands.length && !this._actionHandler && !this._findCommand("help"));
        if (hasImplicitHelpCommand) {
          if (this._helpCommand === void 0) {
            this.helpCommand(void 0, void 0);
          }
          return this._helpCommand;
        }
        return null;
      }
      /**
       * Add hook for life cycle event.
       *
       * @param {string} event
       * @param {Function} listener
       * @return {Command} `this` command for chaining
       */
      hook(event, listener) {
        const allowedValues = ["preSubcommand", "preAction", "postAction"];
        if (!allowedValues.includes(event)) {
          throw new Error(`Unexpected value for event passed to hook : '${event}'.
Expecting one of '${allowedValues.join("', '")}'`);
        }
        if (this._lifeCycleHooks[event]) {
          this._lifeCycleHooks[event].push(listener);
        } else {
          this._lifeCycleHooks[event] = [listener];
        }
        return this;
      }
      /**
       * Register callback to use as replacement for calling process.exit.
       *
       * @param {Function} [fn] optional callback which will be passed a CommanderError, defaults to throwing
       * @return {Command} `this` command for chaining
       */
      exitOverride(fn) {
        if (fn) {
          this._exitCallback = fn;
        } else {
          this._exitCallback = (err) => {
            if (err.code !== "commander.executeSubCommandAsync") {
              throw err;
            } else {
            }
          };
        }
        return this;
      }
      /**
       * Call process.exit, and _exitCallback if defined.
       *
       * @param {number} exitCode exit code for using with process.exit
       * @param {string} code an id string representing the error
       * @param {string} message human-readable description of the error
       * @return never
       * @private
       */
      _exit(exitCode, code, message) {
        if (this._exitCallback) {
          this._exitCallback(new CommanderError2(exitCode, code, message));
        }
        process9.exit(exitCode);
      }
      /**
       * Register callback `fn` for the command.
       *
       * @example
       * program
       *   .command('serve')
       *   .description('start service')
       *   .action(function() {
       *      // do work here
       *   });
       *
       * @param {Function} fn
       * @return {Command} `this` command for chaining
       */
      action(fn) {
        const listener = (args) => {
          const expectedArgsCount = this.registeredArguments.length;
          const actionArgs = args.slice(0, expectedArgsCount);
          if (this._storeOptionsAsProperties) {
            actionArgs[expectedArgsCount] = this;
          } else {
            actionArgs[expectedArgsCount] = this.opts();
          }
          actionArgs.push(this);
          return fn.apply(this, actionArgs);
        };
        this._actionHandler = listener;
        return this;
      }
      /**
       * Factory routine to create a new unattached option.
       *
       * See .option() for creating an attached option, which uses this routine to
       * create the option. You can override createOption to return a custom option.
       *
       * @param {string} flags
       * @param {string} [description]
       * @return {Option} new option
       */
      createOption(flags, description) {
        return new Option2(flags, description);
      }
      /**
       * Wrap parseArgs to catch 'commander.invalidArgument'.
       *
       * @param {(Option | Argument)} target
       * @param {string} value
       * @param {*} previous
       * @param {string} invalidArgumentMessage
       * @private
       */
      _callParseArg(target, value, previous, invalidArgumentMessage) {
        try {
          return target.parseArg(value, previous);
        } catch (err) {
          if (err.code === "commander.invalidArgument") {
            const message = `${invalidArgumentMessage} ${err.message}`;
            this.error(message, { exitCode: err.exitCode, code: err.code });
          }
          throw err;
        }
      }
      /**
       * Check for option flag conflicts.
       * Register option if no conflicts found, or throw on conflict.
       *
       * @param {Option} option
       * @private
       */
      _registerOption(option) {
        const matchingOption = option.short && this._findOption(option.short) || option.long && this._findOption(option.long);
        if (matchingOption) {
          const matchingFlag = option.long && this._findOption(option.long) ? option.long : option.short;
          throw new Error(`Cannot add option '${option.flags}'${this._name && ` to command '${this._name}'`} due to conflicting flag '${matchingFlag}'
-  already used by option '${matchingOption.flags}'`);
        }
        this._initOptionGroup(option);
        this.options.push(option);
      }
      /**
       * Check for command name and alias conflicts with existing commands.
       * Register command if no conflicts found, or throw on conflict.
       *
       * @param {Command} command
       * @private
       */
      _registerCommand(command) {
        const knownBy = (cmd) => {
          return [cmd.name()].concat(cmd.aliases());
        };
        const alreadyUsed = knownBy(command).find(
          (name) => this._findCommand(name)
        );
        if (alreadyUsed) {
          const existingCmd = knownBy(this._findCommand(alreadyUsed)).join("|");
          const newCmd = knownBy(command).join("|");
          throw new Error(
            `cannot add command '${newCmd}' as already have command '${existingCmd}'`
          );
        }
        this._initCommandGroup(command);
        this.commands.push(command);
      }
      /**
       * Add an option.
       *
       * @param {Option} option
       * @return {Command} `this` command for chaining
       */
      addOption(option) {
        this._registerOption(option);
        const oname = option.name();
        const name = option.attributeName();
        if (option.negate) {
          const positiveLongFlag = option.long.replace(/^--no-/, "--");
          if (!this._findOption(positiveLongFlag)) {
            this.setOptionValueWithSource(
              name,
              option.defaultValue === void 0 ? true : option.defaultValue,
              "default"
            );
          }
        } else if (option.defaultValue !== void 0) {
          this.setOptionValueWithSource(name, option.defaultValue, "default");
        }
        const handleOptionValue = (val, invalidValueMessage, valueSource) => {
          if (val == null && option.presetArg !== void 0) {
            val = option.presetArg;
          }
          const oldValue = this.getOptionValue(name);
          if (val !== null && option.parseArg) {
            val = this._callParseArg(option, val, oldValue, invalidValueMessage);
          } else if (val !== null && option.variadic) {
            val = option._collectValue(val, oldValue);
          }
          if (val == null) {
            if (option.negate) {
              val = false;
            } else if (option.isBoolean() || option.optional) {
              val = true;
            } else {
              val = "";
            }
          }
          this.setOptionValueWithSource(name, val, valueSource);
        };
        this.on("option:" + oname, (val) => {
          const invalidValueMessage = `error: option '${option.flags}' argument '${val}' is invalid.`;
          handleOptionValue(val, invalidValueMessage, "cli");
        });
        if (option.envVar) {
          this.on("optionEnv:" + oname, (val) => {
            const invalidValueMessage = `error: option '${option.flags}' value '${val}' from env '${option.envVar}' is invalid.`;
            handleOptionValue(val, invalidValueMessage, "env");
          });
        }
        return this;
      }
      /**
       * Internal implementation shared by .option() and .requiredOption()
       *
       * @return {Command} `this` command for chaining
       * @private
       */
      _optionEx(config2, flags, description, fn, defaultValue) {
        if (typeof flags === "object" && flags instanceof Option2) {
          throw new Error(
            "To add an Option object use addOption() instead of option() or requiredOption()"
          );
        }
        const option = this.createOption(flags, description);
        option.makeOptionMandatory(!!config2.mandatory);
        if (typeof fn === "function") {
          option.default(defaultValue).argParser(fn);
        } else if (fn instanceof RegExp) {
          const regex = fn;
          fn = (val, def) => {
            const m = regex.exec(val);
            return m ? m[0] : def;
          };
          option.default(defaultValue).argParser(fn);
        } else {
          option.default(fn);
        }
        return this.addOption(option);
      }
      /**
       * Define option with `flags`, `description`, and optional argument parsing function or `defaultValue` or both.
       *
       * The `flags` string contains the short and/or long flags, separated by comma, a pipe or space. A required
       * option-argument is indicated by `<>` and an optional option-argument by `[]`.
       *
       * See the README for more details, and see also addOption() and requiredOption().
       *
       * @example
       * program
       *     .option('-p, --pepper', 'add pepper')
       *     .option('--pt, --pizza-type <TYPE>', 'type of pizza') // required option-argument
       *     .option('-c, --cheese [CHEESE]', 'add extra cheese', 'mozzarella') // optional option-argument with default
       *     .option('-t, --tip <VALUE>', 'add tip to purchase cost', parseFloat) // custom parse function
       *
       * @param {string} flags
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom option processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      option(flags, description, parseArg, defaultValue) {
        return this._optionEx({}, flags, description, parseArg, defaultValue);
      }
      /**
       * Add a required option which must have a value after parsing. This usually means
       * the option must be specified on the command line. (Otherwise the same as .option().)
       *
       * The `flags` string contains the short and/or long flags, separated by comma, a pipe or space.
       *
       * @param {string} flags
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom option processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      requiredOption(flags, description, parseArg, defaultValue) {
        return this._optionEx(
          { mandatory: true },
          flags,
          description,
          parseArg,
          defaultValue
        );
      }
      /**
       * Alter parsing of short flags with optional values.
       *
       * @example
       * // for `.option('-f,--flag [value]'):
       * program.combineFlagAndOptionalValue(true);  // `-f80` is treated like `--flag=80`, this is the default behaviour
       * program.combineFlagAndOptionalValue(false) // `-fb` is treated like `-f -b`
       *
       * @param {boolean} [combine] - if `true` or omitted, an optional value can be specified directly after the flag.
       * @return {Command} `this` command for chaining
       */
      combineFlagAndOptionalValue(combine = true) {
        this._combineFlagAndOptionalValue = !!combine;
        return this;
      }
      /**
       * Allow unknown options on the command line.
       *
       * @param {boolean} [allowUnknown] - if `true` or omitted, no error will be thrown for unknown options.
       * @return {Command} `this` command for chaining
       */
      allowUnknownOption(allowUnknown = true) {
        this._allowUnknownOption = !!allowUnknown;
        return this;
      }
      /**
       * Allow excess command-arguments on the command line. Pass false to make excess arguments an error.
       *
       * @param {boolean} [allowExcess] - if `true` or omitted, no error will be thrown for excess arguments.
       * @return {Command} `this` command for chaining
       */
      allowExcessArguments(allowExcess = true) {
        this._allowExcessArguments = !!allowExcess;
        return this;
      }
      /**
       * Enable positional options. Positional means global options are specified before subcommands which lets
       * subcommands reuse the same option names, and also enables subcommands to turn on passThroughOptions.
       * The default behaviour is non-positional and global options may appear anywhere on the command line.
       *
       * @param {boolean} [positional]
       * @return {Command} `this` command for chaining
       */
      enablePositionalOptions(positional = true) {
        this._enablePositionalOptions = !!positional;
        return this;
      }
      /**
       * Pass through options that come after command-arguments rather than treat them as command-options,
       * so actual command-options come before command-arguments. Turning this on for a subcommand requires
       * positional options to have been enabled on the program (parent commands).
       * The default behaviour is non-positional and options may appear before or after command-arguments.
       *
       * @param {boolean} [passThrough] for unknown options.
       * @return {Command} `this` command for chaining
       */
      passThroughOptions(passThrough = true) {
        this._passThroughOptions = !!passThrough;
        this._checkForBrokenPassThrough();
        return this;
      }
      /**
       * @private
       */
      _checkForBrokenPassThrough() {
        if (this.parent && this._passThroughOptions && !this.parent._enablePositionalOptions) {
          throw new Error(
            `passThroughOptions cannot be used for '${this._name}' without turning on enablePositionalOptions for parent command(s)`
          );
        }
      }
      /**
       * Whether to store option values as properties on command object,
       * or store separately (specify false). In both cases the option values can be accessed using .opts().
       *
       * @param {boolean} [storeAsProperties=true]
       * @return {Command} `this` command for chaining
       */
      storeOptionsAsProperties(storeAsProperties = true) {
        if (this.options.length) {
          throw new Error("call .storeOptionsAsProperties() before adding options");
        }
        if (Object.keys(this._optionValues).length) {
          throw new Error(
            "call .storeOptionsAsProperties() before setting option values"
          );
        }
        this._storeOptionsAsProperties = !!storeAsProperties;
        return this;
      }
      /**
       * Retrieve option value.
       *
       * @param {string} key
       * @return {object} value
       */
      getOptionValue(key) {
        if (this._storeOptionsAsProperties) {
          return this[key];
        }
        return this._optionValues[key];
      }
      /**
       * Store option value.
       *
       * @param {string} key
       * @param {object} value
       * @return {Command} `this` command for chaining
       */
      setOptionValue(key, value) {
        return this.setOptionValueWithSource(key, value, void 0);
      }
      /**
       * Store option value and where the value came from.
       *
       * @param {string} key
       * @param {object} value
       * @param {string} source - expected values are default/config/env/cli/implied
       * @return {Command} `this` command for chaining
       */
      setOptionValueWithSource(key, value, source) {
        if (this._storeOptionsAsProperties) {
          this[key] = value;
        } else {
          this._optionValues[key] = value;
        }
        this._optionValueSources[key] = source;
        return this;
      }
      /**
       * Get source of option value.
       * Expected values are default | config | env | cli | implied
       *
       * @param {string} key
       * @return {string}
       */
      getOptionValueSource(key) {
        return this._optionValueSources[key];
      }
      /**
       * Get source of option value. See also .optsWithGlobals().
       * Expected values are default | config | env | cli | implied
       *
       * @param {string} key
       * @return {string}
       */
      getOptionValueSourceWithGlobals(key) {
        let source;
        this._getCommandAndAncestors().forEach((cmd) => {
          if (cmd.getOptionValueSource(key) !== void 0) {
            source = cmd.getOptionValueSource(key);
          }
        });
        return source;
      }
      /**
       * Get user arguments from implied or explicit arguments.
       * Side-effects: set _scriptPath if args included script. Used for default program name, and subcommand searches.
       *
       * @private
       */
      _prepareUserArgs(argv, parseOptions) {
        if (argv !== void 0 && !Array.isArray(argv)) {
          throw new Error("first parameter to parse must be array or undefined");
        }
        parseOptions = parseOptions || {};
        if (argv === void 0 && parseOptions.from === void 0) {
          if (process9.versions?.electron) {
            parseOptions.from = "electron";
          }
          const execArgv = process9.execArgv ?? [];
          if (execArgv.includes("-e") || execArgv.includes("--eval") || execArgv.includes("-p") || execArgv.includes("--print")) {
            parseOptions.from = "eval";
          }
        }
        if (argv === void 0) {
          argv = process9.argv;
        }
        this.rawArgs = argv.slice();
        let userArgs;
        switch (parseOptions.from) {
          case void 0:
          case "node":
            this._scriptPath = argv[1];
            userArgs = argv.slice(2);
            break;
          case "electron":
            if (process9.defaultApp) {
              this._scriptPath = argv[1];
              userArgs = argv.slice(2);
            } else {
              userArgs = argv.slice(1);
            }
            break;
          case "user":
            userArgs = argv.slice(0);
            break;
          case "eval":
            userArgs = argv.slice(1);
            break;
          default:
            throw new Error(
              `unexpected parse option { from: '${parseOptions.from}' }`
            );
        }
        if (!this._name && this._scriptPath)
          this.nameFromFilename(this._scriptPath);
        this._name = this._name || "program";
        return userArgs;
      }
      /**
       * Parse `argv`, setting options and invoking commands when defined.
       *
       * Use parseAsync instead of parse if any of your action handlers are async.
       *
       * Call with no parameters to parse `process.argv`. Detects Electron and special node options like `node --eval`. Easy mode!
       *
       * Or call with an array of strings to parse, and optionally where the user arguments start by specifying where the arguments are `from`:
       * - `'node'`: default, `argv[0]` is the application and `argv[1]` is the script being run, with user arguments after that
       * - `'electron'`: `argv[0]` is the application and `argv[1]` varies depending on whether the electron application is packaged
       * - `'user'`: just user arguments
       *
       * @example
       * program.parse(); // parse process.argv and auto-detect electron and special node flags
       * program.parse(process.argv); // assume argv[0] is app and argv[1] is script
       * program.parse(my-args, { from: 'user' }); // just user supplied arguments, nothing special about argv[0]
       *
       * @param {string[]} [argv] - optional, defaults to process.argv
       * @param {object} [parseOptions] - optionally specify style of options with from: node/user/electron
       * @param {string} [parseOptions.from] - where the args are from: 'node', 'user', 'electron'
       * @return {Command} `this` command for chaining
       */
      parse(argv, parseOptions) {
        this._prepareForParse();
        const userArgs = this._prepareUserArgs(argv, parseOptions);
        this._parseCommand([], userArgs);
        return this;
      }
      /**
       * Parse `argv`, setting options and invoking commands when defined.
       *
       * Call with no parameters to parse `process.argv`. Detects Electron and special node options like `node --eval`. Easy mode!
       *
       * Or call with an array of strings to parse, and optionally where the user arguments start by specifying where the arguments are `from`:
       * - `'node'`: default, `argv[0]` is the application and `argv[1]` is the script being run, with user arguments after that
       * - `'electron'`: `argv[0]` is the application and `argv[1]` varies depending on whether the electron application is packaged
       * - `'user'`: just user arguments
       *
       * @example
       * await program.parseAsync(); // parse process.argv and auto-detect electron and special node flags
       * await program.parseAsync(process.argv); // assume argv[0] is app and argv[1] is script
       * await program.parseAsync(my-args, { from: 'user' }); // just user supplied arguments, nothing special about argv[0]
       *
       * @param {string[]} [argv]
       * @param {object} [parseOptions]
       * @param {string} parseOptions.from - where the args are from: 'node', 'user', 'electron'
       * @return {Promise}
       */
      async parseAsync(argv, parseOptions) {
        this._prepareForParse();
        const userArgs = this._prepareUserArgs(argv, parseOptions);
        await this._parseCommand([], userArgs);
        return this;
      }
      _prepareForParse() {
        if (this._savedState === null) {
          this.saveStateBeforeParse();
        } else {
          this.restoreStateBeforeParse();
        }
      }
      /**
       * Called the first time parse is called to save state and allow a restore before subsequent calls to parse.
       * Not usually called directly, but available for subclasses to save their custom state.
       *
       * This is called in a lazy way. Only commands used in parsing chain will have state saved.
       */
      saveStateBeforeParse() {
        this._savedState = {
          // name is stable if supplied by author, but may be unspecified for root command and deduced during parsing
          _name: this._name,
          // option values before parse have default values (including false for negated options)
          // shallow clones
          _optionValues: { ...this._optionValues },
          _optionValueSources: { ...this._optionValueSources }
        };
      }
      /**
       * Restore state before parse for calls after the first.
       * Not usually called directly, but available for subclasses to save their custom state.
       *
       * This is called in a lazy way. Only commands used in parsing chain will have state restored.
       */
      restoreStateBeforeParse() {
        if (this._storeOptionsAsProperties)
          throw new Error(`Can not call parse again when storeOptionsAsProperties is true.
- either make a new Command for each call to parse, or stop storing options as properties`);
        this._name = this._savedState._name;
        this._scriptPath = null;
        this.rawArgs = [];
        this._optionValues = { ...this._savedState._optionValues };
        this._optionValueSources = { ...this._savedState._optionValueSources };
        this.args = [];
        this.processedArgs = [];
      }
      /**
       * Throw if expected executable is missing. Add lots of help for author.
       *
       * @param {string} executableFile
       * @param {string} executableDir
       * @param {string} subcommandName
       */
      _checkForMissingExecutable(executableFile, executableDir, subcommandName) {
        if (fs7.existsSync(executableFile)) return;
        const executableDirMessage = executableDir ? `searched for local subcommand relative to directory '${executableDir}'` : "no directory for search for local subcommand, use .executableDir() to supply a custom directory";
        const executableMissing = `'${executableFile}' does not exist
 - if '${subcommandName}' is not meant to be an executable command, remove description parameter from '.command()' and use '.description()' instead
 - if the default executable name is not suitable, use the executableFile option to supply a custom name or path
 - ${executableDirMessage}`;
        throw new Error(executableMissing);
      }
      /**
       * Execute a sub-command executable.
       *
       * @private
       */
      _executeSubCommand(subcommand, args) {
        args = args.slice();
        let launchWithNode = false;
        const sourceExt = [".js", ".ts", ".tsx", ".mjs", ".cjs"];
        function findFile(baseDir, baseName) {
          const localBin = path5.resolve(baseDir, baseName);
          if (fs7.existsSync(localBin)) return localBin;
          if (sourceExt.includes(path5.extname(baseName))) return void 0;
          const foundExt = sourceExt.find(
            (ext) => fs7.existsSync(`${localBin}${ext}`)
          );
          if (foundExt) return `${localBin}${foundExt}`;
          return void 0;
        }
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        let executableFile = subcommand._executableFile || `${this._name}-${subcommand._name}`;
        let executableDir = this._executableDir || "";
        if (this._scriptPath) {
          let resolvedScriptPath;
          try {
            resolvedScriptPath = fs7.realpathSync(this._scriptPath);
          } catch {
            resolvedScriptPath = this._scriptPath;
          }
          executableDir = path5.resolve(
            path5.dirname(resolvedScriptPath),
            executableDir
          );
        }
        if (executableDir) {
          let localFile = findFile(executableDir, executableFile);
          if (!localFile && !subcommand._executableFile && this._scriptPath) {
            const legacyName = path5.basename(
              this._scriptPath,
              path5.extname(this._scriptPath)
            );
            if (legacyName !== this._name) {
              localFile = findFile(
                executableDir,
                `${legacyName}-${subcommand._name}`
              );
            }
          }
          executableFile = localFile || executableFile;
        }
        launchWithNode = sourceExt.includes(path5.extname(executableFile));
        let proc;
        if (process9.platform !== "win32") {
          if (launchWithNode) {
            args.unshift(executableFile);
            args = incrementNodeInspectorPort(process9.execArgv).concat(args);
            proc = childProcess4.spawn(process9.argv[0], args, { stdio: "inherit" });
          } else {
            proc = childProcess4.spawn(executableFile, args, { stdio: "inherit" });
          }
        } else {
          this._checkForMissingExecutable(
            executableFile,
            executableDir,
            subcommand._name
          );
          args.unshift(executableFile);
          args = incrementNodeInspectorPort(process9.execArgv).concat(args);
          proc = childProcess4.spawn(process9.execPath, args, { stdio: "inherit" });
        }
        if (!proc.killed) {
          const signals = ["SIGUSR1", "SIGUSR2", "SIGTERM", "SIGINT", "SIGHUP"];
          signals.forEach((signal) => {
            process9.on(signal, () => {
              if (proc.killed === false && proc.exitCode === null) {
                proc.kill(signal);
              }
            });
          });
        }
        const exitCallback = this._exitCallback;
        proc.on("close", (code) => {
          code = code ?? 1;
          if (!exitCallback) {
            process9.exit(code);
          } else {
            exitCallback(
              new CommanderError2(
                code,
                "commander.executeSubCommandAsync",
                "(close)"
              )
            );
          }
        });
        proc.on("error", (err) => {
          if (err.code === "ENOENT") {
            this._checkForMissingExecutable(
              executableFile,
              executableDir,
              subcommand._name
            );
          } else if (err.code === "EACCES") {
            throw new Error(`'${executableFile}' not executable`);
          }
          if (!exitCallback) {
            process9.exit(1);
          } else {
            const wrappedError = new CommanderError2(
              1,
              "commander.executeSubCommandAsync",
              "(error)"
            );
            wrappedError.nestedError = err;
            exitCallback(wrappedError);
          }
        });
        this.runningCommand = proc;
      }
      /**
       * @private
       */
      _dispatchSubcommand(commandName, operands, unknown) {
        const subCommand = this._findCommand(commandName);
        if (!subCommand) this.help({ error: true });
        subCommand._prepareForParse();
        let promiseChain;
        promiseChain = this._chainOrCallSubCommandHook(
          promiseChain,
          subCommand,
          "preSubcommand"
        );
        promiseChain = this._chainOrCall(promiseChain, () => {
          if (subCommand._executableHandler) {
            this._executeSubCommand(subCommand, operands.concat(unknown));
          } else {
            return subCommand._parseCommand(operands, unknown);
          }
        });
        return promiseChain;
      }
      /**
       * Invoke help directly if possible, or dispatch if necessary.
       * e.g. help foo
       *
       * @private
       */
      _dispatchHelpCommand(subcommandName) {
        if (!subcommandName) {
          this.help();
        }
        const subCommand = this._findCommand(subcommandName);
        if (subCommand && !subCommand._executableHandler) {
          subCommand.help();
        }
        return this._dispatchSubcommand(
          subcommandName,
          [],
          [this._getHelpOption()?.long ?? this._getHelpOption()?.short ?? "--help"]
        );
      }
      /**
       * Check this.args against expected this.registeredArguments.
       *
       * @private
       */
      _checkNumberOfArguments() {
        this.registeredArguments.forEach((arg, i) => {
          if (arg.required && this.args[i] == null) {
            this.missingArgument(arg.name());
          }
        });
        if (this.registeredArguments.length > 0 && this.registeredArguments[this.registeredArguments.length - 1].variadic) {
          return;
        }
        if (this.args.length > this.registeredArguments.length) {
          this._excessArguments(this.args);
        }
      }
      /**
       * Process this.args using this.registeredArguments and save as this.processedArgs!
       *
       * @private
       */
      _processArguments() {
        const myParseArg = (argument, value, previous) => {
          let parsedValue = value;
          if (value !== null && argument.parseArg) {
            const invalidValueMessage = `error: command-argument value '${value}' is invalid for argument '${argument.name()}'.`;
            parsedValue = this._callParseArg(
              argument,
              value,
              previous,
              invalidValueMessage
            );
          }
          return parsedValue;
        };
        this._checkNumberOfArguments();
        const processedArgs = [];
        this.registeredArguments.forEach((declaredArg, index) => {
          let value = declaredArg.defaultValue;
          if (declaredArg.variadic) {
            if (index < this.args.length) {
              value = this.args.slice(index);
              if (declaredArg.parseArg) {
                value = value.reduce((processed, v) => {
                  return myParseArg(declaredArg, v, processed);
                }, declaredArg.defaultValue);
              }
            } else if (value === void 0) {
              value = [];
            }
          } else if (index < this.args.length) {
            value = this.args[index];
            if (declaredArg.parseArg) {
              value = myParseArg(declaredArg, value, declaredArg.defaultValue);
            }
          }
          processedArgs[index] = value;
        });
        this.processedArgs = processedArgs;
      }
      /**
       * Once we have a promise we chain, but call synchronously until then.
       *
       * @param {(Promise|undefined)} promise
       * @param {Function} fn
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCall(promise, fn) {
        if (promise?.then && typeof promise.then === "function") {
          return promise.then(() => fn());
        }
        return fn();
      }
      /**
       *
       * @param {(Promise|undefined)} promise
       * @param {string} event
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCallHooks(promise, event) {
        let result = promise;
        const hooks = [];
        this._getCommandAndAncestors().reverse().filter((cmd) => cmd._lifeCycleHooks[event] !== void 0).forEach((hookedCommand) => {
          hookedCommand._lifeCycleHooks[event].forEach((callback) => {
            hooks.push({ hookedCommand, callback });
          });
        });
        if (event === "postAction") {
          hooks.reverse();
        }
        hooks.forEach((hookDetail) => {
          result = this._chainOrCall(result, () => {
            return hookDetail.callback(hookDetail.hookedCommand, this);
          });
        });
        return result;
      }
      /**
       *
       * @param {(Promise|undefined)} promise
       * @param {Command} subCommand
       * @param {string} event
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCallSubCommandHook(promise, subCommand, event) {
        let result = promise;
        if (this._lifeCycleHooks[event] !== void 0) {
          this._lifeCycleHooks[event].forEach((hook) => {
            result = this._chainOrCall(result, () => {
              return hook(this, subCommand);
            });
          });
        }
        return result;
      }
      /**
       * Process arguments in context of this command.
       * Returns action result, in case it is a promise.
       *
       * @private
       */
      _parseCommand(operands, unknown) {
        const parsed2 = this.parseOptions(unknown);
        this._parseOptionsEnv();
        this._parseOptionsImplied();
        operands = operands.concat(parsed2.operands);
        unknown = parsed2.unknown;
        this.args = operands.concat(unknown);
        if (operands && this._findCommand(operands[0])) {
          return this._dispatchSubcommand(operands[0], operands.slice(1), unknown);
        }
        if (this._getHelpCommand() && operands[0] === this._getHelpCommand().name()) {
          return this._dispatchHelpCommand(operands[1]);
        }
        if (this._defaultCommandName) {
          this._outputHelpIfRequested(unknown);
          return this._dispatchSubcommand(
            this._defaultCommandName,
            operands,
            unknown
          );
        }
        if (this.commands.length && this.args.length === 0 && !this._actionHandler && !this._defaultCommandName) {
          this.help({ error: true });
        }
        this._outputHelpIfRequested(parsed2.unknown);
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        const checkForUnknownOptions = () => {
          if (parsed2.unknown.length > 0) {
            this.unknownOption(parsed2.unknown[0]);
          }
        };
        const commandEvent = `command:${this.name()}`;
        if (this._actionHandler) {
          checkForUnknownOptions();
          this._processArguments();
          let promiseChain;
          promiseChain = this._chainOrCallHooks(promiseChain, "preAction");
          promiseChain = this._chainOrCall(
            promiseChain,
            () => this._actionHandler(this.processedArgs)
          );
          if (this.parent) {
            promiseChain = this._chainOrCall(promiseChain, () => {
              this.parent.emit(commandEvent, operands, unknown);
            });
          }
          promiseChain = this._chainOrCallHooks(promiseChain, "postAction");
          return promiseChain;
        }
        if (this.parent?.listenerCount(commandEvent)) {
          checkForUnknownOptions();
          this._processArguments();
          this.parent.emit(commandEvent, operands, unknown);
        } else if (operands.length) {
          if (this._findCommand("*")) {
            return this._dispatchSubcommand("*", operands, unknown);
          }
          if (this.listenerCount("command:*")) {
            this.emit("command:*", operands, unknown);
          } else if (this.commands.length) {
            this.unknownCommand();
          } else {
            checkForUnknownOptions();
            this._processArguments();
          }
        } else if (this.commands.length) {
          checkForUnknownOptions();
          this.help({ error: true });
        } else {
          checkForUnknownOptions();
          this._processArguments();
        }
      }
      /**
       * Find matching command.
       *
       * @private
       * @return {Command | undefined}
       */
      _findCommand(name) {
        if (!name) return void 0;
        return this.commands.find(
          (cmd) => cmd._name === name || cmd._aliases.includes(name)
        );
      }
      /**
       * Return an option matching `arg` if any.
       *
       * @param {string} arg
       * @return {Option}
       * @package
       */
      _findOption(arg) {
        return this.options.find((option) => option.is(arg));
      }
      /**
       * Display an error message if a mandatory option does not have a value.
       * Called after checking for help flags in leaf subcommand.
       *
       * @private
       */
      _checkForMissingMandatoryOptions() {
        this._getCommandAndAncestors().forEach((cmd) => {
          cmd.options.forEach((anOption) => {
            if (anOption.mandatory && cmd.getOptionValue(anOption.attributeName()) === void 0) {
              cmd.missingMandatoryOptionValue(anOption);
            }
          });
        });
      }
      /**
       * Display an error message if conflicting options are used together in this.
       *
       * @private
       */
      _checkForConflictingLocalOptions() {
        const definedNonDefaultOptions = this.options.filter((option) => {
          const optionKey = option.attributeName();
          if (this.getOptionValue(optionKey) === void 0) {
            return false;
          }
          return this.getOptionValueSource(optionKey) !== "default";
        });
        const optionsWithConflicting = definedNonDefaultOptions.filter(
          (option) => option.conflictsWith.length > 0
        );
        optionsWithConflicting.forEach((option) => {
          const conflictingAndDefined = definedNonDefaultOptions.find(
            (defined) => option.conflictsWith.includes(defined.attributeName())
          );
          if (conflictingAndDefined) {
            this._conflictingOption(option, conflictingAndDefined);
          }
        });
      }
      /**
       * Display an error message if conflicting options are used together.
       * Called after checking for help flags in leaf subcommand.
       *
       * @private
       */
      _checkForConflictingOptions() {
        this._getCommandAndAncestors().forEach((cmd) => {
          cmd._checkForConflictingLocalOptions();
        });
      }
      /**
       * Parse options from `argv` removing known options,
       * and return argv split into operands and unknown arguments.
       *
       * Side effects: modifies command by storing options. Does not reset state if called again.
       *
       * Examples:
       *
       *     argv => operands, unknown
       *     --known kkk op => [op], []
       *     op --known kkk => [op], []
       *     sub --unknown uuu op => [sub], [--unknown uuu op]
       *     sub -- --unknown uuu op => [sub --unknown uuu op], []
       *
       * @param {string[]} args
       * @return {{operands: string[], unknown: string[]}}
       */
      parseOptions(args) {
        const operands = [];
        const unknown = [];
        let dest = operands;
        function maybeOption(arg) {
          return arg.length > 1 && arg[0] === "-";
        }
        const negativeNumberArg = (arg) => {
          if (!/^-(\d+|\d*\.\d+)(e[+-]?\d+)?$/.test(arg)) return false;
          return !this._getCommandAndAncestors().some(
            (cmd) => cmd.options.map((opt) => opt.short).some((short) => /^-\d$/.test(short))
          );
        };
        let activeVariadicOption = null;
        let activeGroup = null;
        let i = 0;
        while (i < args.length || activeGroup) {
          const arg = activeGroup ?? args[i++];
          activeGroup = null;
          if (arg === "--") {
            if (dest === unknown) dest.push(arg);
            dest.push(...args.slice(i));
            break;
          }
          if (activeVariadicOption && (!maybeOption(arg) || negativeNumberArg(arg))) {
            this.emit(`option:${activeVariadicOption.name()}`, arg);
            continue;
          }
          activeVariadicOption = null;
          if (maybeOption(arg)) {
            const option = this._findOption(arg);
            if (option) {
              if (option.required) {
                const value = args[i++];
                if (value === void 0) this.optionMissingArgument(option);
                this.emit(`option:${option.name()}`, value);
              } else if (option.optional) {
                let value = null;
                if (i < args.length && (!maybeOption(args[i]) || negativeNumberArg(args[i]))) {
                  value = args[i++];
                }
                this.emit(`option:${option.name()}`, value);
              } else {
                this.emit(`option:${option.name()}`);
              }
              activeVariadicOption = option.variadic ? option : null;
              continue;
            }
          }
          if (arg.length > 2 && arg[0] === "-" && arg[1] !== "-") {
            const option = this._findOption(`-${arg[1]}`);
            if (option) {
              if (option.required || option.optional && this._combineFlagAndOptionalValue) {
                this.emit(`option:${option.name()}`, arg.slice(2));
              } else {
                this.emit(`option:${option.name()}`);
                activeGroup = `-${arg.slice(2)}`;
              }
              continue;
            }
          }
          if (/^--[^=]+=/.test(arg)) {
            const index = arg.indexOf("=");
            const option = this._findOption(arg.slice(0, index));
            if (option && (option.required || option.optional)) {
              this.emit(`option:${option.name()}`, arg.slice(index + 1));
              continue;
            }
          }
          if (dest === operands && maybeOption(arg) && !(this.commands.length === 0 && negativeNumberArg(arg))) {
            dest = unknown;
          }
          if ((this._enablePositionalOptions || this._passThroughOptions) && operands.length === 0 && unknown.length === 0) {
            if (this._findCommand(arg)) {
              operands.push(arg);
              unknown.push(...args.slice(i));
              break;
            } else if (this._getHelpCommand() && arg === this._getHelpCommand().name()) {
              operands.push(arg, ...args.slice(i));
              break;
            } else if (this._defaultCommandName) {
              unknown.push(arg, ...args.slice(i));
              break;
            }
          }
          if (this._passThroughOptions) {
            dest.push(arg, ...args.slice(i));
            break;
          }
          dest.push(arg);
        }
        return { operands, unknown };
      }
      /**
       * Return an object containing local option values as key-value pairs.
       *
       * @return {object}
       */
      opts() {
        if (this._storeOptionsAsProperties) {
          const result = {};
          const len = this.options.length;
          for (let i = 0; i < len; i++) {
            const key = this.options[i].attributeName();
            result[key] = key === this._versionOptionName ? this._version : this[key];
          }
          return result;
        }
        return this._optionValues;
      }
      /**
       * Return an object containing merged local and global option values as key-value pairs.
       *
       * @return {object}
       */
      optsWithGlobals() {
        return this._getCommandAndAncestors().reduce(
          (combinedOptions, cmd) => Object.assign(combinedOptions, cmd.opts()),
          {}
        );
      }
      /**
       * Display error message and exit (or call exitOverride).
       *
       * @param {string} message
       * @param {object} [errorOptions]
       * @param {string} [errorOptions.code] - an id string representing the error
       * @param {number} [errorOptions.exitCode] - used with process.exit
       */
      error(message, errorOptions) {
        this._outputConfiguration.outputError(
          `${message}
`,
          this._outputConfiguration.writeErr
        );
        if (typeof this._showHelpAfterError === "string") {
          this._outputConfiguration.writeErr(`${this._showHelpAfterError}
`);
        } else if (this._showHelpAfterError) {
          this._outputConfiguration.writeErr("\n");
          this.outputHelp({ error: true });
        }
        const config2 = errorOptions || {};
        const exitCode = config2.exitCode || 1;
        const code = config2.code || "commander.error";
        this._exit(exitCode, code, message);
      }
      /**
       * Apply any option related environment variables, if option does
       * not have a value from cli or client code.
       *
       * @private
       */
      _parseOptionsEnv() {
        this.options.forEach((option) => {
          if (option.envVar && option.envVar in process9.env) {
            const optionKey = option.attributeName();
            if (this.getOptionValue(optionKey) === void 0 || ["default", "config", "env"].includes(
              this.getOptionValueSource(optionKey)
            )) {
              if (option.required || option.optional) {
                this.emit(`optionEnv:${option.name()}`, process9.env[option.envVar]);
              } else {
                this.emit(`optionEnv:${option.name()}`);
              }
            }
          }
        });
      }
      /**
       * Apply any implied option values, if option is undefined or default value.
       *
       * @private
       */
      _parseOptionsImplied() {
        const dualHelper = new DualOptions(this.options);
        const hasCustomOptionValue = (optionKey) => {
          return this.getOptionValue(optionKey) !== void 0 && !["default", "implied"].includes(this.getOptionValueSource(optionKey));
        };
        this.options.filter(
          (option) => option.implied !== void 0 && hasCustomOptionValue(option.attributeName()) && dualHelper.valueFromOption(
            this.getOptionValue(option.attributeName()),
            option
          )
        ).forEach((option) => {
          Object.keys(option.implied).filter((impliedKey) => !hasCustomOptionValue(impliedKey)).forEach((impliedKey) => {
            this.setOptionValueWithSource(
              impliedKey,
              option.implied[impliedKey],
              "implied"
            );
          });
        });
      }
      /**
       * Argument `name` is missing.
       *
       * @param {string} name
       * @private
       */
      missingArgument(name) {
        const message = `error: missing required argument '${name}'`;
        this.error(message, { code: "commander.missingArgument" });
      }
      /**
       * `Option` is missing an argument.
       *
       * @param {Option} option
       * @private
       */
      optionMissingArgument(option) {
        const message = `error: option '${option.flags}' argument missing`;
        this.error(message, { code: "commander.optionMissingArgument" });
      }
      /**
       * `Option` does not have a value, and is a mandatory option.
       *
       * @param {Option} option
       * @private
       */
      missingMandatoryOptionValue(option) {
        const message = `error: required option '${option.flags}' not specified`;
        this.error(message, { code: "commander.missingMandatoryOptionValue" });
      }
      /**
       * `Option` conflicts with another option.
       *
       * @param {Option} option
       * @param {Option} conflictingOption
       * @private
       */
      _conflictingOption(option, conflictingOption) {
        const findBestOptionFromValue = (option2) => {
          const optionKey = option2.attributeName();
          const optionValue = this.getOptionValue(optionKey);
          const negativeOption = this.options.find(
            (target) => target.negate && optionKey === target.attributeName()
          );
          const positiveOption = this.options.find(
            (target) => !target.negate && optionKey === target.attributeName()
          );
          if (negativeOption && (negativeOption.presetArg === void 0 && optionValue === false || negativeOption.presetArg !== void 0 && optionValue === negativeOption.presetArg)) {
            return negativeOption;
          }
          return positiveOption || option2;
        };
        const getErrorMessage = (option2) => {
          const bestOption = findBestOptionFromValue(option2);
          const optionKey = bestOption.attributeName();
          const source = this.getOptionValueSource(optionKey);
          if (source === "env") {
            return `environment variable '${bestOption.envVar}'`;
          }
          return `option '${bestOption.flags}'`;
        };
        const message = `error: ${getErrorMessage(option)} cannot be used with ${getErrorMessage(conflictingOption)}`;
        this.error(message, { code: "commander.conflictingOption" });
      }
      /**
       * Unknown option `flag`.
       *
       * @param {string} flag
       * @private
       */
      unknownOption(flag) {
        if (this._allowUnknownOption) return;
        let suggestion = "";
        if (flag.startsWith("--") && this._showSuggestionAfterError) {
          let candidateFlags = [];
          let command = this;
          do {
            const moreFlags = command.createHelp().visibleOptions(command).filter((option) => option.long).map((option) => option.long);
            candidateFlags = candidateFlags.concat(moreFlags);
            command = command.parent;
          } while (command && !command._enablePositionalOptions);
          suggestion = suggestSimilar(flag, candidateFlags);
        }
        const message = `error: unknown option '${flag}'${suggestion}`;
        this.error(message, { code: "commander.unknownOption" });
      }
      /**
       * Excess arguments, more than expected.
       *
       * @param {string[]} receivedArgs
       * @private
       */
      _excessArguments(receivedArgs) {
        if (this._allowExcessArguments) return;
        const expected = this.registeredArguments.length;
        const s = expected === 1 ? "" : "s";
        const forSubcommand = this.parent ? ` for '${this.name()}'` : "";
        const message = `error: too many arguments${forSubcommand}. Expected ${expected} argument${s} but got ${receivedArgs.length}.`;
        this.error(message, { code: "commander.excessArguments" });
      }
      /**
       * Unknown command.
       *
       * @private
       */
      unknownCommand() {
        const unknownName = this.args[0];
        let suggestion = "";
        if (this._showSuggestionAfterError) {
          const candidateNames = [];
          this.createHelp().visibleCommands(this).forEach((command) => {
            candidateNames.push(command.name());
            if (command.alias()) candidateNames.push(command.alias());
          });
          suggestion = suggestSimilar(unknownName, candidateNames);
        }
        const message = `error: unknown command '${unknownName}'${suggestion}`;
        this.error(message, { code: "commander.unknownCommand" });
      }
      /**
       * Get or set the program version.
       *
       * This method auto-registers the "-V, --version" option which will print the version number.
       *
       * You can optionally supply the flags and description to override the defaults.
       *
       * @param {string} [str]
       * @param {string} [flags]
       * @param {string} [description]
       * @return {(this | string | undefined)} `this` command for chaining, or version string if no arguments
       */
      version(str, flags, description) {
        if (str === void 0) return this._version;
        this._version = str;
        flags = flags || "-V, --version";
        description = description || "output the version number";
        const versionOption = this.createOption(flags, description);
        this._versionOptionName = versionOption.attributeName();
        this._registerOption(versionOption);
        this.on("option:" + versionOption.name(), () => {
          this._outputConfiguration.writeOut(`${str}
`);
          this._exit(0, "commander.version", str);
        });
        return this;
      }
      /**
       * Set the description.
       *
       * @param {string} [str]
       * @param {object} [argsDescription]
       * @return {(string|Command)}
       */
      description(str, argsDescription) {
        if (str === void 0 && argsDescription === void 0)
          return this._description;
        this._description = str;
        if (argsDescription) {
          this._argsDescription = argsDescription;
        }
        return this;
      }
      /**
       * Set the summary. Used when listed as subcommand of parent.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      summary(str) {
        if (str === void 0) return this._summary;
        this._summary = str;
        return this;
      }
      /**
       * Set an alias for the command.
       *
       * You may call more than once to add multiple aliases. Only the first alias is shown in the auto-generated help.
       *
       * @param {string} [alias]
       * @return {(string|Command)}
       */
      alias(alias) {
        if (alias === void 0) return this._aliases[0];
        let command = this;
        if (this.commands.length !== 0 && this.commands[this.commands.length - 1]._executableHandler) {
          command = this.commands[this.commands.length - 1];
        }
        if (alias === command._name)
          throw new Error("Command alias can't be the same as its name");
        const matchingCommand = this.parent?._findCommand(alias);
        if (matchingCommand) {
          const existingCmd = [matchingCommand.name()].concat(matchingCommand.aliases()).join("|");
          throw new Error(
            `cannot add alias '${alias}' to command '${this.name()}' as already have command '${existingCmd}'`
          );
        }
        command._aliases.push(alias);
        return this;
      }
      /**
       * Set aliases for the command.
       *
       * Only the first alias is shown in the auto-generated help.
       *
       * @param {string[]} [aliases]
       * @return {(string[]|Command)}
       */
      aliases(aliases) {
        if (aliases === void 0) return this._aliases;
        aliases.forEach((alias) => this.alias(alias));
        return this;
      }
      /**
       * Set / get the command usage `str`.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      usage(str) {
        if (str === void 0) {
          if (this._usage) return this._usage;
          const args = this.registeredArguments.map((arg) => {
            return humanReadableArgName(arg);
          });
          return [].concat(
            this.options.length || this._helpOption !== null ? "[options]" : [],
            this.commands.length ? "[command]" : [],
            this.registeredArguments.length ? args : []
          ).join(" ");
        }
        this._usage = str;
        return this;
      }
      /**
       * Get or set the name of the command.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      name(str) {
        if (str === void 0) return this._name;
        this._name = str;
        return this;
      }
      /**
       * Set/get the help group heading for this subcommand in parent command's help.
       *
       * @param {string} [heading]
       * @return {Command | string}
       */
      helpGroup(heading) {
        if (heading === void 0) return this._helpGroupHeading ?? "";
        this._helpGroupHeading = heading;
        return this;
      }
      /**
       * Set/get the default help group heading for subcommands added to this command.
       * (This does not override a group set directly on the subcommand using .helpGroup().)
       *
       * @example
       * program.commandsGroup('Development Commands:);
       * program.command('watch')...
       * program.command('lint')...
       * ...
       *
       * @param {string} [heading]
       * @returns {Command | string}
       */
      commandsGroup(heading) {
        if (heading === void 0) return this._defaultCommandGroup ?? "";
        this._defaultCommandGroup = heading;
        return this;
      }
      /**
       * Set/get the default help group heading for options added to this command.
       * (This does not override a group set directly on the option using .helpGroup().)
       *
       * @example
       * program
       *   .optionsGroup('Development Options:')
       *   .option('-d, --debug', 'output extra debugging')
       *   .option('-p, --profile', 'output profiling information')
       *
       * @param {string} [heading]
       * @returns {Command | string}
       */
      optionsGroup(heading) {
        if (heading === void 0) return this._defaultOptionGroup ?? "";
        this._defaultOptionGroup = heading;
        return this;
      }
      /**
       * @param {Option} option
       * @private
       */
      _initOptionGroup(option) {
        if (this._defaultOptionGroup && !option.helpGroupHeading)
          option.helpGroup(this._defaultOptionGroup);
      }
      /**
       * @param {Command} cmd
       * @private
       */
      _initCommandGroup(cmd) {
        if (this._defaultCommandGroup && !cmd.helpGroup())
          cmd.helpGroup(this._defaultCommandGroup);
      }
      /**
       * Set the name of the command from script filename, such as process.argv[1],
       * or require.main.filename, or __filename.
       *
       * (Used internally and public although not documented in README.)
       *
       * @example
       * program.nameFromFilename(require.main.filename);
       *
       * @param {string} filename
       * @return {Command}
       */
      nameFromFilename(filename) {
        this._name = path5.basename(filename, path5.extname(filename));
        return this;
      }
      /**
       * Get or set the directory for searching for executable subcommands of this command.
       *
       * @example
       * program.executableDir(__dirname);
       * // or
       * program.executableDir('subcommands');
       *
       * @param {string} [path]
       * @return {(string|null|Command)}
       */
      executableDir(path6) {
        if (path6 === void 0) return this._executableDir;
        this._executableDir = path6;
        return this;
      }
      /**
       * Return program help documentation.
       *
       * @param {{ error: boolean }} [contextOptions] - pass {error:true} to wrap for stderr instead of stdout
       * @return {string}
       */
      helpInformation(contextOptions) {
        const helper = this.createHelp();
        const context = this._getOutputContext(contextOptions);
        helper.prepareContext({
          error: context.error,
          helpWidth: context.helpWidth,
          outputHasColors: context.hasColors
        });
        const text = helper.formatHelp(this, helper);
        if (context.hasColors) return text;
        return this._outputConfiguration.stripColor(text);
      }
      /**
       * @typedef HelpContext
       * @type {object}
       * @property {boolean} error
       * @property {number} helpWidth
       * @property {boolean} hasColors
       * @property {function} write - includes stripColor if needed
       *
       * @returns {HelpContext}
       * @private
       */
      _getOutputContext(contextOptions) {
        contextOptions = contextOptions || {};
        const error = !!contextOptions.error;
        let baseWrite;
        let hasColors;
        let helpWidth;
        if (error) {
          baseWrite = (str) => this._outputConfiguration.writeErr(str);
          hasColors = this._outputConfiguration.getErrHasColors();
          helpWidth = this._outputConfiguration.getErrHelpWidth();
        } else {
          baseWrite = (str) => this._outputConfiguration.writeOut(str);
          hasColors = this._outputConfiguration.getOutHasColors();
          helpWidth = this._outputConfiguration.getOutHelpWidth();
        }
        const write = (str) => {
          if (!hasColors) str = this._outputConfiguration.stripColor(str);
          return baseWrite(str);
        };
        return { error, write, hasColors, helpWidth };
      }
      /**
       * Output help information for this command.
       *
       * Outputs built-in help, and custom text added using `.addHelpText()`.
       *
       * @param {{ error: boolean } | Function} [contextOptions] - pass {error:true} to write to stderr instead of stdout
       */
      outputHelp(contextOptions) {
        let deprecatedCallback;
        if (typeof contextOptions === "function") {
          deprecatedCallback = contextOptions;
          contextOptions = void 0;
        }
        const outputContext = this._getOutputContext(contextOptions);
        const eventContext = {
          error: outputContext.error,
          write: outputContext.write,
          command: this
        };
        this._getCommandAndAncestors().reverse().forEach((command) => command.emit("beforeAllHelp", eventContext));
        this.emit("beforeHelp", eventContext);
        let helpInformation = this.helpInformation({ error: outputContext.error });
        if (deprecatedCallback) {
          helpInformation = deprecatedCallback(helpInformation);
          if (typeof helpInformation !== "string" && !Buffer.isBuffer(helpInformation)) {
            throw new Error("outputHelp callback must return a string or a Buffer");
          }
        }
        outputContext.write(helpInformation);
        if (this._getHelpOption()?.long) {
          this.emit(this._getHelpOption().long);
        }
        this.emit("afterHelp", eventContext);
        this._getCommandAndAncestors().forEach(
          (command) => command.emit("afterAllHelp", eventContext)
        );
      }
      /**
       * You can pass in flags and a description to customise the built-in help option.
       * Pass in false to disable the built-in help option.
       *
       * @example
       * program.helpOption('-?, --help' 'show help'); // customise
       * program.helpOption(false); // disable
       *
       * @param {(string | boolean)} flags
       * @param {string} [description]
       * @return {Command} `this` command for chaining
       */
      helpOption(flags, description) {
        if (typeof flags === "boolean") {
          if (flags) {
            if (this._helpOption === null) this._helpOption = void 0;
            if (this._defaultOptionGroup) {
              this._initOptionGroup(this._getHelpOption());
            }
          } else {
            this._helpOption = null;
          }
          return this;
        }
        this._helpOption = this.createOption(
          flags ?? "-h, --help",
          description ?? "display help for command"
        );
        if (flags || description) this._initOptionGroup(this._helpOption);
        return this;
      }
      /**
       * Lazy create help option.
       * Returns null if has been disabled with .helpOption(false).
       *
       * @returns {(Option | null)} the help option
       * @package
       */
      _getHelpOption() {
        if (this._helpOption === void 0) {
          this.helpOption(void 0, void 0);
        }
        return this._helpOption;
      }
      /**
       * Supply your own option to use for the built-in help option.
       * This is an alternative to using helpOption() to customise the flags and description etc.
       *
       * @param {Option} option
       * @return {Command} `this` command for chaining
       */
      addHelpOption(option) {
        this._helpOption = option;
        this._initOptionGroup(option);
        return this;
      }
      /**
       * Output help information and exit.
       *
       * Outputs built-in help, and custom text added using `.addHelpText()`.
       *
       * @param {{ error: boolean }} [contextOptions] - pass {error:true} to write to stderr instead of stdout
       */
      help(contextOptions) {
        this.outputHelp(contextOptions);
        let exitCode = Number(process9.exitCode ?? 0);
        if (exitCode === 0 && contextOptions && typeof contextOptions !== "function" && contextOptions.error) {
          exitCode = 1;
        }
        this._exit(exitCode, "commander.help", "(outputHelp)");
      }
      /**
       * // Do a little typing to coordinate emit and listener for the help text events.
       * @typedef HelpTextEventContext
       * @type {object}
       * @property {boolean} error
       * @property {Command} command
       * @property {function} write
       */
      /**
       * Add additional text to be displayed with the built-in help.
       *
       * Position is 'before' or 'after' to affect just this command,
       * and 'beforeAll' or 'afterAll' to affect this command and all its subcommands.
       *
       * @param {string} position - before or after built-in help
       * @param {(string | Function)} text - string to add, or a function returning a string
       * @return {Command} `this` command for chaining
       */
      addHelpText(position, text) {
        const allowedValues = ["beforeAll", "before", "after", "afterAll"];
        if (!allowedValues.includes(position)) {
          throw new Error(`Unexpected value for position to addHelpText.
Expecting one of '${allowedValues.join("', '")}'`);
        }
        const helpEvent = `${position}Help`;
        this.on(helpEvent, (context) => {
          let helpStr;
          if (typeof text === "function") {
            helpStr = text({ error: context.error, command: context.command });
          } else {
            helpStr = text;
          }
          if (helpStr) {
            context.write(`${helpStr}
`);
          }
        });
        return this;
      }
      /**
       * Output help information if help flags specified
       *
       * @param {Array} args - array of options to search for help flags
       * @private
       */
      _outputHelpIfRequested(args) {
        const helpOption = this._getHelpOption();
        const helpRequested = helpOption && args.find((arg) => helpOption.is(arg));
        if (helpRequested) {
          this.outputHelp();
          this._exit(0, "commander.helpDisplayed", "(outputHelp)");
        }
      }
    };
    function incrementNodeInspectorPort(args) {
      return args.map((arg) => {
        if (!arg.startsWith("--inspect")) {
          return arg;
        }
        let debugOption;
        let debugHost = "127.0.0.1";
        let debugPort = "9229";
        let match;
        if ((match = arg.match(/^(--inspect(-brk)?)$/)) !== null) {
          debugOption = match[1];
        } else if ((match = arg.match(/^(--inspect(-brk|-port)?)=([^:]+)$/)) !== null) {
          debugOption = match[1];
          if (/^\d+$/.test(match[3])) {
            debugPort = match[3];
          } else {
            debugHost = match[3];
          }
        } else if ((match = arg.match(/^(--inspect(-brk|-port)?)=([^:]+):(\d+)$/)) !== null) {
          debugOption = match[1];
          debugHost = match[3];
          debugPort = match[4];
        }
        if (debugOption && debugPort !== "0") {
          return `${debugOption}=${debugHost}:${parseInt(debugPort) + 1}`;
        }
        return arg;
      });
    }
    function useColor() {
      if (process9.env.NO_COLOR || process9.env.FORCE_COLOR === "0" || process9.env.FORCE_COLOR === "false")
        return false;
      if (process9.env.FORCE_COLOR || process9.env.CLICOLOR_FORCE !== void 0)
        return true;
      return void 0;
    }
    exports2.Command = Command2;
    exports2.useColor = useColor;
  }
});

// node_modules/commander/index.js
var require_commander = __commonJS({
  "node_modules/commander/index.js"(exports2) {
    var { Argument: Argument2 } = require_argument();
    var { Command: Command2 } = require_command();
    var { CommanderError: CommanderError2, InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var { Help: Help2 } = require_help();
    var { Option: Option2 } = require_option();
    exports2.program = new Command2();
    exports2.createCommand = (name) => new Command2(name);
    exports2.createOption = (flags, description) => new Option2(flags, description);
    exports2.createArgument = (name, description) => new Argument2(name, description);
    exports2.Command = Command2;
    exports2.Option = Option2;
    exports2.Argument = Argument2;
    exports2.Help = Help2;
    exports2.CommanderError = CommanderError2;
    exports2.InvalidArgumentError = InvalidArgumentError2;
    exports2.InvalidOptionArgumentError = InvalidArgumentError2;
  }
});

// node_modules/http-message-signatures/lib/errors/verification-error.js
var require_verification_error = __commonJS({
  "node_modules/http-message-signatures/lib/errors/verification-error.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.VerificationError = void 0;
    var VerificationError = class extends Error {
    };
    exports2.VerificationError = VerificationError;
  }
});

// node_modules/http-message-signatures/lib/errors/expired-error.js
var require_expired_error = __commonJS({
  "node_modules/http-message-signatures/lib/errors/expired-error.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.ExpiredError = void 0;
    var verification_error_1 = require_verification_error();
    var ExpiredError = class extends verification_error_1.VerificationError {
    };
    exports2.ExpiredError = ExpiredError;
  }
});

// node_modules/http-message-signatures/lib/errors/malformed-signature-error.js
var require_malformed_signature_error = __commonJS({
  "node_modules/http-message-signatures/lib/errors/malformed-signature-error.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.MalformedSignatureError = void 0;
    var verification_error_1 = require_verification_error();
    var MalformedSignatureError = class extends verification_error_1.VerificationError {
    };
    exports2.MalformedSignatureError = MalformedSignatureError;
  }
});

// node_modules/http-message-signatures/lib/errors/unacceptable-signature-error.js
var require_unacceptable_signature_error = __commonJS({
  "node_modules/http-message-signatures/lib/errors/unacceptable-signature-error.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.UnacceptableSignatureError = void 0;
    var verification_error_1 = require_verification_error();
    var UnacceptableSignatureError = class extends verification_error_1.VerificationError {
    };
    exports2.UnacceptableSignatureError = UnacceptableSignatureError;
  }
});

// node_modules/http-message-signatures/lib/errors/unknown-algorithm-error.js
var require_unknown_algorithm_error = __commonJS({
  "node_modules/http-message-signatures/lib/errors/unknown-algorithm-error.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.UnknownAlgorithmError = void 0;
    var UnknownAlgorithmError = class extends Error {
    };
    exports2.UnknownAlgorithmError = UnknownAlgorithmError;
  }
});

// node_modules/http-message-signatures/lib/errors/unknown-key-error.js
var require_unknown_key_error = __commonJS({
  "node_modules/http-message-signatures/lib/errors/unknown-key-error.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.UnknownKeyError = void 0;
    var verification_error_1 = require_verification_error();
    var UnknownKeyError = class extends verification_error_1.VerificationError {
    };
    exports2.UnknownKeyError = UnknownKeyError;
  }
});

// node_modules/http-message-signatures/lib/errors/unsupported-algorithm-error.js
var require_unsupported_algorithm_error = __commonJS({
  "node_modules/http-message-signatures/lib/errors/unsupported-algorithm-error.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.UnsupportedAlgorithmError = void 0;
    var verification_error_1 = require_verification_error();
    var UnsupportedAlgorithmError = class extends verification_error_1.VerificationError {
    };
    exports2.UnsupportedAlgorithmError = UnsupportedAlgorithmError;
  }
});

// node_modules/http-message-signatures/lib/errors/index.js
var require_errors = __commonJS({
  "node_modules/http-message-signatures/lib/errors/index.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.VerificationError = exports2.UnsupportedAlgorithmError = exports2.UnknownKeyError = exports2.UnknownAlgorithmError = exports2.UnacceptableSignatureError = exports2.MalformedSignatureError = exports2.ExpiredError = void 0;
    var expired_error_1 = require_expired_error();
    Object.defineProperty(exports2, "ExpiredError", { enumerable: true, get: function() {
      return expired_error_1.ExpiredError;
    } });
    var malformed_signature_error_1 = require_malformed_signature_error();
    Object.defineProperty(exports2, "MalformedSignatureError", { enumerable: true, get: function() {
      return malformed_signature_error_1.MalformedSignatureError;
    } });
    var unacceptable_signature_error_1 = require_unacceptable_signature_error();
    Object.defineProperty(exports2, "UnacceptableSignatureError", { enumerable: true, get: function() {
      return unacceptable_signature_error_1.UnacceptableSignatureError;
    } });
    var unknown_algorithm_error_1 = require_unknown_algorithm_error();
    Object.defineProperty(exports2, "UnknownAlgorithmError", { enumerable: true, get: function() {
      return unknown_algorithm_error_1.UnknownAlgorithmError;
    } });
    var unknown_key_error_1 = require_unknown_key_error();
    Object.defineProperty(exports2, "UnknownKeyError", { enumerable: true, get: function() {
      return unknown_key_error_1.UnknownKeyError;
    } });
    var unsupported_algorithm_error_1 = require_unsupported_algorithm_error();
    Object.defineProperty(exports2, "UnsupportedAlgorithmError", { enumerable: true, get: function() {
      return unsupported_algorithm_error_1.UnsupportedAlgorithmError;
    } });
    var verification_error_1 = require_verification_error();
    Object.defineProperty(exports2, "VerificationError", { enumerable: true, get: function() {
      return verification_error_1.VerificationError;
    } });
  }
});

// node_modules/http-message-signatures/lib/algorithm/index.js
var require_algorithm = __commonJS({
  "node_modules/http-message-signatures/lib/algorithm/index.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.createVerifier = exports2.createSigner = void 0;
    var crypto_1 = require("crypto");
    var constants_1 = require("constants");
    var errors_1 = require_errors();
    function createSigner2(key, alg, id) {
      const signer = { alg };
      switch (alg) {
        case "hmac-sha256":
          signer.sign = async (data) => (0, crypto_1.createHmac)("sha256", key).update(data).digest();
          break;
        case "rsa-pss-sha512":
          signer.sign = async (data) => (0, crypto_1.createSign)("sha512").update(data).sign({
            key,
            padding: constants_1.RSA_PKCS1_PSS_PADDING
          });
          break;
        case "rsa-v1_5-sha256":
          signer.sign = async (data) => (0, crypto_1.createSign)("sha256").update(data).sign({
            key,
            padding: constants_1.RSA_PKCS1_PADDING
          });
          break;
        case "rsa-v1_5-sha1":
          signer.sign = async (data) => (0, crypto_1.createSign)("sha1").update(data).sign({
            key,
            padding: constants_1.RSA_PKCS1_PADDING
          });
          break;
        case "ecdsa-p256-sha256":
          signer.sign = async (data) => (0, crypto_1.createSign)("sha256").update(data).sign({
            key,
            dsaEncoding: "ieee-p1363"
          });
          break;
        case "ecdsa-p384-sha384":
          signer.sign = async (data) => (0, crypto_1.createSign)("sha384").update(data).sign({
            key,
            dsaEncoding: "ieee-p1363"
          });
          break;
        case "ed25519":
          signer.sign = async (data) => (0, crypto_1.sign)(null, data, key);
          break;
        default:
          throw new errors_1.UnknownAlgorithmError(`Unsupported signing algorithm ${alg}`);
      }
      if (id) {
        signer.id = id;
      }
      return signer;
    }
    exports2.createSigner = createSigner2;
    function createVerifier(key, alg) {
      let verifier;
      switch (alg) {
        case "hmac-sha256":
          verifier = async (data, signature) => {
            const expected = (0, crypto_1.createHmac)("sha256", key).update(data).digest();
            return signature.length === expected.length && (0, crypto_1.timingSafeEqual)(signature, expected);
          };
          break;
        case "rsa-pss-sha512":
          verifier = async (data, signature) => (0, crypto_1.createVerify)("sha512").update(data).verify({
            key,
            padding: constants_1.RSA_PKCS1_PSS_PADDING
          }, signature);
          break;
        case "rsa-v1_5-sha1":
          verifier = async (data, signature) => (0, crypto_1.createVerify)("sha1").update(data).verify({
            key,
            padding: constants_1.RSA_PKCS1_PADDING
          }, signature);
          break;
        case "rsa-v1_5-sha256":
          verifier = async (data, signature) => (0, crypto_1.createVerify)("sha256").update(data).verify({
            key,
            padding: constants_1.RSA_PKCS1_PADDING
          }, signature);
          break;
        case "ecdsa-p256-sha256":
          verifier = async (data, signature) => (0, crypto_1.createVerify)("sha256").update(data).verify({
            key,
            dsaEncoding: "ieee-p1363"
          }, signature);
          break;
        case "ecdsa-p384-sha384":
          verifier = async (data, signature) => (0, crypto_1.createVerify)("sha384").update(data).verify({
            key,
            dsaEncoding: "ieee-p1363"
          }, signature);
          break;
        case "ed25519":
          verifier = async (data, signature) => (0, crypto_1.verify)(null, data, key, signature);
          break;
        default:
          throw new errors_1.UnknownAlgorithmError(`Unsupported signing algorithm ${alg}`);
      }
      return Object.assign(verifier, { alg });
    }
    exports2.createVerifier = createVerifier;
  }
});

// node_modules/http-message-signatures/lib/types/index.js
var require_types = __commonJS({
  "node_modules/http-message-signatures/lib/types/index.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isRequest = exports2.defaultParams = void 0;
    exports2.defaultParams = [
      "keyid",
      "alg",
      "created",
      "expires"
    ];
    function isRequest(obj) {
      return !!obj.method;
    }
    exports2.isRequest = isRequest;
  }
});

// node_modules/structured-headers/dist/types.js
var require_types2 = __commonJS({
  "node_modules/structured-headers/dist/types.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.ByteSequence = void 0;
    var ByteSequence = class {
      constructor(base64Value) {
        this.base64Value = base64Value;
      }
      toBase64() {
        return this.base64Value;
      }
    };
    exports2.ByteSequence = ByteSequence;
  }
});

// node_modules/structured-headers/dist/util.js
var require_util = __commonJS({
  "node_modules/structured-headers/dist/util.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isByteSequence = exports2.isInnerList = exports2.isValidKeyStr = exports2.isValidTokenStr = exports2.isAscii = void 0;
    var asciiRe = /^[\x20-\x7E]*$/;
    var tokenRe = /^[a-zA-Z*][:/!#$%&'*+\-.^_`|~A-Za-z0-9]*$/;
    var keyRe = /^[a-z*][*\-_.a-z0-9]*$/;
    function isAscii(str) {
      return asciiRe.test(str);
    }
    exports2.isAscii = isAscii;
    function isValidTokenStr(str) {
      return tokenRe.test(str);
    }
    exports2.isValidTokenStr = isValidTokenStr;
    function isValidKeyStr(str) {
      return keyRe.test(str);
    }
    exports2.isValidKeyStr = isValidKeyStr;
    function isInnerList(input) {
      return Array.isArray(input[0]);
    }
    exports2.isInnerList = isInnerList;
    function isByteSequence(input) {
      return typeof input === "object" && "base64Value" in input;
    }
    exports2.isByteSequence = isByteSequence;
  }
});

// node_modules/structured-headers/dist/token.js
var require_token = __commonJS({
  "node_modules/structured-headers/dist/token.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.Token = void 0;
    var util_1 = require_util();
    var Token = class {
      constructor(value) {
        if (!(0, util_1.isValidTokenStr)(value)) {
          throw new TypeError("Invalid character in Token string. Tokens must start with *, A-Z and the rest of the string may only contain a-z, A-Z, 0-9, :/!#$%&'*+-.^_`|~");
        }
        this.value = value;
      }
      toString() {
        return this.value;
      }
    };
    exports2.Token = Token;
  }
});

// node_modules/structured-headers/dist/serializer.js
var require_serializer = __commonJS({
  "node_modules/structured-headers/dist/serializer.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.serializeKey = exports2.serializeParameters = exports2.serializeToken = exports2.serializeByteSequence = exports2.serializeBoolean = exports2.serializeString = exports2.serializeDecimal = exports2.serializeInteger = exports2.serializeBareItem = exports2.serializeInnerList = exports2.serializeItem = exports2.serializeDictionary = exports2.serializeList = exports2.SerializeError = void 0;
    var types_1 = require_types2();
    var token_1 = require_token();
    var util_1 = require_util();
    var SerializeError = class extends Error {
    };
    exports2.SerializeError = SerializeError;
    function serializeList(input) {
      return input.map((value) => {
        if ((0, util_1.isInnerList)(value)) {
          return serializeInnerList(value);
        } else {
          return serializeItem(value);
        }
      }).join(", ");
    }
    exports2.serializeList = serializeList;
    function serializeDictionary(input) {
      return Array.from(input.entries()).map(([key, value]) => {
        let out = serializeKey(key);
        if (value[0] === true) {
          out += serializeParameters(value[1]);
        } else {
          out += "=";
          if ((0, util_1.isInnerList)(value)) {
            out += serializeInnerList(value);
          } else {
            out += serializeItem(value);
          }
        }
        return out;
      }).join(", ");
    }
    exports2.serializeDictionary = serializeDictionary;
    function serializeItem(input) {
      return serializeBareItem(input[0]) + serializeParameters(input[1]);
    }
    exports2.serializeItem = serializeItem;
    function serializeInnerList(input) {
      return `(${input[0].map((value) => serializeItem(value)).join(" ")})${serializeParameters(input[1])}`;
    }
    exports2.serializeInnerList = serializeInnerList;
    function serializeBareItem(input) {
      if (typeof input === "number") {
        if (Number.isInteger(input)) {
          return serializeInteger(input);
        }
        return serializeDecimal(input);
      }
      if (typeof input === "string") {
        return serializeString(input);
      }
      if (input instanceof token_1.Token) {
        return serializeToken(input);
      }
      if (input instanceof types_1.ByteSequence) {
        return serializeByteSequence(input);
      }
      if (typeof input === "boolean") {
        return serializeBoolean(input);
      }
      throw new SerializeError(`Cannot serialize values of type ${typeof input}`);
    }
    exports2.serializeBareItem = serializeBareItem;
    function serializeInteger(input) {
      if (input < -999999999999999 || input > 999999999999999) {
        throw new SerializeError("Structured headers can only encode integers in the range range of -999,999,999,999,999 to 999,999,999,999,999 inclusive");
      }
      return input.toString();
    }
    exports2.serializeInteger = serializeInteger;
    function serializeDecimal(input) {
      const out = input.toFixed(3).replace(/0+$/, "");
      const signifantDigits = out.split(".")[0].replace("-", "").length;
      if (signifantDigits > 12) {
        throw new SerializeError("Fractional numbers are not allowed to have more than 12 significant digits before the decimal point");
      }
      return out;
    }
    exports2.serializeDecimal = serializeDecimal;
    function serializeString(input) {
      if (!(0, util_1.isAscii)(input)) {
        throw new SerializeError("Only ASCII strings may be serialized");
      }
      return `"${input.replace(/("|\\)/g, (v) => "\\" + v)}"`;
    }
    exports2.serializeString = serializeString;
    function serializeBoolean(input) {
      return input ? "?1" : "?0";
    }
    exports2.serializeBoolean = serializeBoolean;
    function serializeByteSequence(input) {
      return `:${input.toBase64()}:`;
    }
    exports2.serializeByteSequence = serializeByteSequence;
    function serializeToken(input) {
      return input.toString();
    }
    exports2.serializeToken = serializeToken;
    function serializeParameters(input) {
      return Array.from(input).map(([key, value]) => {
        let out = ";" + serializeKey(key);
        if (value !== true) {
          out += "=" + serializeBareItem(value);
        }
        return out;
      }).join("");
    }
    exports2.serializeParameters = serializeParameters;
    function serializeKey(input) {
      if (!(0, util_1.isValidKeyStr)(input)) {
        throw new SerializeError("Keys in dictionaries must only contain lowercase letter, numbers, _-*. and must start with a letter or *");
      }
      return input;
    }
    exports2.serializeKey = serializeKey;
  }
});

// node_modules/structured-headers/dist/parser.js
var require_parser = __commonJS({
  "node_modules/structured-headers/dist/parser.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.ParseError = exports2.parseItem = exports2.parseList = exports2.parseDictionary = void 0;
    var types_1 = require_types2();
    var token_1 = require_token();
    var util_1 = require_util();
    function parseDictionary(input) {
      const parser = new Parser(input);
      return parser.parseDictionary();
    }
    exports2.parseDictionary = parseDictionary;
    function parseList(input) {
      const parser = new Parser(input);
      return parser.parseList();
    }
    exports2.parseList = parseList;
    function parseItem(input) {
      const parser = new Parser(input);
      return parser.parseItem();
    }
    exports2.parseItem = parseItem;
    var ParseError2 = class extends Error {
      constructor(position, message) {
        super(`Parse error: ${message} at offset ${position}`);
      }
    };
    exports2.ParseError = ParseError2;
    var Parser = class {
      constructor(input) {
        this.input = input;
        this.pos = 0;
      }
      parseDictionary() {
        this.skipWS();
        const dictionary = /* @__PURE__ */ new Map();
        while (!this.eof()) {
          const thisKey = this.parseKey();
          let member;
          if (this.lookChar() === "=") {
            this.pos++;
            member = this.parseItemOrInnerList();
          } else {
            member = [true, this.parseParameters()];
          }
          dictionary.set(thisKey, member);
          this.skipOWS();
          if (this.eof()) {
            return dictionary;
          }
          this.expectChar(",");
          this.pos++;
          this.skipOWS();
          if (this.eof()) {
            throw new ParseError2(this.pos, "Dictionary contained a trailing comma");
          }
        }
        return dictionary;
      }
      parseList() {
        this.skipWS();
        const members = [];
        while (!this.eof()) {
          members.push(this.parseItemOrInnerList());
          this.skipOWS();
          if (this.eof()) {
            return members;
          }
          this.expectChar(",");
          this.pos++;
          this.skipOWS();
          if (this.eof()) {
            throw new ParseError2(this.pos, "A list may not end with a trailing comma");
          }
        }
        return members;
      }
      parseItem(standaloneItem = true) {
        if (standaloneItem)
          this.skipWS();
        const result = [
          this.parseBareItem(),
          this.parseParameters()
        ];
        if (standaloneItem)
          this.checkTrail();
        return result;
      }
      parseItemOrInnerList() {
        if (this.lookChar() === "(") {
          return this.parseInnerList();
        } else {
          return this.parseItem(false);
        }
      }
      parseInnerList() {
        this.expectChar("(");
        this.pos++;
        const innerList = [];
        while (!this.eof()) {
          this.skipWS();
          if (this.lookChar() === ")") {
            this.pos++;
            return [
              innerList,
              this.parseParameters()
            ];
          }
          innerList.push(this.parseItem(false));
          const nextChar = this.lookChar();
          if (nextChar !== " " && nextChar !== ")") {
            throw new ParseError2(this.pos, "Expected a whitespace or ) after every item in an inner list");
          }
        }
        throw new ParseError2(this.pos, "Could not find end of inner list");
      }
      parseBareItem() {
        const char = this.lookChar();
        if (char === void 0) {
          throw new ParseError2(this.pos, "Unexpected end of string");
        }
        if (char.match(/^[-0-9]/)) {
          return this.parseIntegerOrDecimal();
        }
        if (char === '"') {
          return this.parseString();
        }
        if (char.match(/^[A-Za-z*]/)) {
          return this.parseToken();
        }
        if (char === ":") {
          return this.parseByteSequence();
        }
        if (char === "?") {
          return this.parseBoolean();
        }
        throw new ParseError2(this.pos, "Unexpected input");
      }
      parseParameters() {
        const parameters = /* @__PURE__ */ new Map();
        while (!this.eof()) {
          const char = this.lookChar();
          if (char !== ";") {
            break;
          }
          this.pos++;
          this.skipWS();
          const key = this.parseKey();
          let value = true;
          if (this.lookChar() === "=") {
            this.pos++;
            value = this.parseBareItem();
          }
          parameters.set(key, value);
        }
        return parameters;
      }
      parseIntegerOrDecimal() {
        let type = "integer";
        let sign = 1;
        let inputNumber = "";
        if (this.lookChar() === "-") {
          sign = -1;
          this.pos++;
        }
        if (!isDigit(this.lookChar())) {
          throw new ParseError2(this.pos, "Expected a digit (0-9)");
        }
        while (!this.eof()) {
          const char = this.getChar();
          if (isDigit(char)) {
            inputNumber += char;
          } else if (type === "integer" && char === ".") {
            if (inputNumber.length > 12) {
              throw new ParseError2(this.pos, "Exceeded maximum decimal length");
            }
            inputNumber += ".";
            type = "decimal";
          } else {
            this.pos--;
            break;
          }
          if (type === "integer" && inputNumber.length > 15) {
            throw new ParseError2(this.pos, "Exceeded maximum integer length");
          }
          if (type === "decimal" && inputNumber.length > 16) {
            throw new ParseError2(this.pos, "Exceeded maximum decimal length");
          }
        }
        if (type === "integer") {
          return parseInt(inputNumber, 10) * sign;
        } else {
          if (inputNumber.endsWith(".")) {
            throw new ParseError2(this.pos, "Decimal cannot end on a period");
          }
          if (inputNumber.split(".")[1].length > 3) {
            throw new ParseError2(this.pos, "Number of digits after the decimal point cannot exceed 3");
          }
          return parseFloat(inputNumber) * sign;
        }
      }
      parseString() {
        let outputString = "";
        this.expectChar('"');
        this.pos++;
        while (!this.eof()) {
          const char = this.getChar();
          if (char === "\\") {
            if (this.eof()) {
              throw new ParseError2(this.pos, "Unexpected end of input");
            }
            const nextChar = this.getChar();
            if (nextChar !== "\\" && nextChar !== '"') {
              throw new ParseError2(this.pos, "A backslash must be followed by another backslash or double quote");
            }
            outputString += nextChar;
          } else if (char === '"') {
            return outputString;
          } else if (!(0, util_1.isAscii)(char)) {
            throw new ParseError2(this.pos, "Strings must be in the ASCII range");
          } else {
            outputString += char;
          }
        }
        throw new ParseError2(this.pos, "Unexpected end of input");
      }
      parseToken() {
        let outputString = "";
        while (!this.eof()) {
          const char = this.lookChar();
          if (char === void 0 || !/^[:/!#$%&'*+\-.^_`|~A-Za-z0-9]$/.test(char)) {
            return new token_1.Token(outputString);
          }
          outputString += this.getChar();
        }
        return new token_1.Token(outputString);
      }
      parseByteSequence() {
        this.expectChar(":");
        this.pos++;
        const endPos = this.input.indexOf(":", this.pos);
        if (endPos === -1) {
          throw new ParseError2(this.pos, 'Could not find a closing ":" character to mark end of Byte Sequence');
        }
        const b64Content = this.input.substring(this.pos, endPos);
        this.pos += b64Content.length + 1;
        if (!/^[A-Za-z0-9+/=]*$/.test(b64Content)) {
          throw new ParseError2(this.pos, "ByteSequence does not contain a valid base64 string");
        }
        return new types_1.ByteSequence(b64Content);
      }
      parseBoolean() {
        this.expectChar("?");
        this.pos++;
        const char = this.getChar();
        if (char === "1") {
          return true;
        }
        if (char === "0") {
          return false;
        }
        throw new ParseError2(this.pos, 'Unexpected character. Expected a "1" or a "0"');
      }
      parseKey() {
        var _a;
        if (!((_a = this.lookChar()) === null || _a === void 0 ? void 0 : _a.match(/^[a-z*]/))) {
          throw new ParseError2(this.pos, "A key must begin with an asterisk or letter (a-z)");
        }
        let outputString = "";
        while (!this.eof()) {
          const char = this.lookChar();
          if (char === void 0 || !/^[a-z0-9_\-.*]$/.test(char)) {
            return outputString;
          }
          outputString += this.getChar();
        }
        return outputString;
      }
      /**
       * Looks at the next character without advancing the cursor.
       *
       * Returns undefined if we were at the end of the string.
       */
      lookChar() {
        return this.input[this.pos];
      }
      /**
       * Checks if the next character is 'char', and fail otherwise.
       */
      expectChar(char) {
        if (this.lookChar() !== char) {
          throw new ParseError2(this.pos, `Expected ${char}`);
        }
      }
      getChar() {
        return this.input[this.pos++];
      }
      eof() {
        return this.pos >= this.input.length;
      }
      // Advances the pointer to skip all whitespace.
      skipOWS() {
        while (true) {
          const c = this.input.substr(this.pos, 1);
          if (c === " " || c === "	") {
            this.pos++;
          } else {
            break;
          }
        }
      }
      // Advances the pointer to skip all spaces
      skipWS() {
        while (this.lookChar() === " ") {
          this.pos++;
        }
      }
      // At the end of parsing, we need to make sure there are no bytes after the
      // header except whitespace.
      checkTrail() {
        this.skipWS();
        if (!this.eof()) {
          throw new ParseError2(this.pos, "Unexpected characters at end of input");
        }
      }
    };
    exports2.default = Parser;
    var isDigitRegex = /^[0-9]$/;
    function isDigit(char) {
      if (char === void 0)
        return false;
      return isDigitRegex.test(char);
    }
  }
});

// node_modules/structured-headers/dist/index.js
var require_dist = __commonJS({
  "node_modules/structured-headers/dist/index.js"(exports2) {
    "use strict";
    var __createBinding = exports2 && exports2.__createBinding || (Object.create ? (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      var desc = Object.getOwnPropertyDescriptor(m, k);
      if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
        desc = { enumerable: true, get: function() {
          return m[k];
        } };
      }
      Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    }));
    var __exportStar = exports2 && exports2.__exportStar || function(m, exports3) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports3, p)) __createBinding(exports3, m, p);
    };
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.Token = void 0;
    __exportStar(require_serializer(), exports2);
    __exportStar(require_parser(), exports2);
    __exportStar(require_types2(), exports2);
    __exportStar(require_util(), exports2);
    var token_1 = require_token();
    Object.defineProperty(exports2, "Token", { enumerable: true, get: function() {
      return token_1.Token;
    } });
  }
});

// node_modules/http-message-signatures/lib/structured-header.js
var require_structured_header = __commonJS({
  "node_modules/http-message-signatures/lib/structured-header.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.quoteString = exports2.parseHeader = exports2.Item = exports2.List = exports2.Dictionary = void 0;
    var structured_headers_1 = require_dist();
    var Dictionary = class {
      constructor(input) {
        this.raw = input;
        this.parsed = (0, structured_headers_1.parseDictionary)(input);
      }
      toString() {
        return this.serialize();
      }
      serialize() {
        return (0, structured_headers_1.serializeDictionary)(this.parsed);
      }
      has(key) {
        return this.parsed.has(key);
      }
      get(key) {
        const value = this.parsed.get(key);
        if (!value) {
          return value;
        }
        if ((0, structured_headers_1.isInnerList)(value)) {
          return (0, structured_headers_1.serializeInnerList)(value);
        }
        return (0, structured_headers_1.serializeItem)(value);
      }
    };
    exports2.Dictionary = Dictionary;
    var List = class {
      constructor(input) {
        this.raw = input;
        this.parsed = (0, structured_headers_1.parseList)(input);
      }
      toString() {
        return this.serialize();
      }
      serialize() {
        return (0, structured_headers_1.serializeList)(this.parsed);
      }
    };
    exports2.List = List;
    var Item = class {
      constructor(input) {
        this.raw = input;
        this.parsed = (0, structured_headers_1.parseItem)(input);
      }
      toString() {
        return this.serialize();
      }
      serialize() {
        return (0, structured_headers_1.serializeItem)(this.parsed);
      }
    };
    exports2.Item = Item;
    function parseHeader(header) {
      const classes = [List, Dictionary, Item];
      for (let i = 0; i < classes.length; i++) {
        try {
          return new classes[i](header);
        } catch (e) {
        }
      }
      throw new Error("Unable to parse header as structured field");
    }
    exports2.parseHeader = parseHeader;
    function quoteString(input) {
      if (!input.startsWith('"')) {
        const [name, ...rest] = input.split(";");
        if (!rest.length) {
          return `"${name}"`;
        }
        return `"${name}";${rest.join(";")}`;
      }
      return input;
    }
    exports2.quoteString = quoteString;
  }
});

// node_modules/http-message-signatures/lib/httpbis/index.js
var require_httpbis = __commonJS({
  "node_modules/http-message-signatures/lib/httpbis/index.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.verifyMessage = exports2.signMessage = exports2.augmentHeaders = exports2.createSigningParameters = exports2.formatSignatureBase = exports2.createSignatureBase = exports2.extractHeader = exports2.deriveComponent = void 0;
    var structured_headers_1 = require_dist();
    var structured_header_1 = require_structured_header();
    var types_1 = require_types();
    var errors_1 = require_errors();
    function deriveComponent(component, params, message, req) {
      const context = params.has("req") ? req : message;
      if (!context) {
        throw new Error("Missing request in request-response bound component");
      }
      switch (component) {
        case "@method":
          if (!(0, types_1.isRequest)(context)) {
            throw new Error("Cannot derive @method from response");
          }
          return [context.method.toUpperCase()];
        case "@target-uri": {
          if (!(0, types_1.isRequest)(context)) {
            throw new Error("Cannot derive @target-uri on response");
          }
          return [context.url.toString()];
        }
        case "@authority": {
          if (!(0, types_1.isRequest)(context)) {
            throw new Error("Cannot derive @authority on response");
          }
          const { port, protocol, hostname } = typeof context.url === "string" ? new URL(context.url) : context.url;
          let authority = hostname.toLowerCase();
          if (port && (protocol === "http:" && port !== "80" || protocol === "https:" && port !== "443")) {
            authority += `:${port}`;
          }
          return [authority];
        }
        case "@scheme": {
          if (!(0, types_1.isRequest)(context)) {
            throw new Error("Cannot derive @scheme on response");
          }
          const { protocol } = typeof context.url === "string" ? new URL(context.url) : context.url;
          return [protocol.slice(0, -1)];
        }
        case "@request-target": {
          if (!(0, types_1.isRequest)(context)) {
            throw new Error("Cannot derive @request-target on response");
          }
          const { pathname, search } = typeof context.url === "string" ? new URL(context.url) : context.url;
          return [`${pathname}${search}`];
        }
        case "@path": {
          if (!(0, types_1.isRequest)(context)) {
            throw new Error("Cannot derive @scheme on response");
          }
          const { pathname } = typeof context.url === "string" ? new URL(context.url) : context.url;
          return [pathname || "/"];
        }
        case "@query": {
          if (!(0, types_1.isRequest)(context)) {
            throw new Error("Cannot derive @scheme on response");
          }
          const { search } = typeof context.url === "string" ? new URL(context.url) : context.url;
          return [search || "?"];
        }
        case "@query-param": {
          if (!(0, types_1.isRequest)(context)) {
            throw new Error("Cannot derive @scheme on response");
          }
          const { searchParams } = typeof context.url === "string" ? new URL(context.url) : context.url;
          if (!params.has("name")) {
            throw new Error("@query-param must have a named parameter");
          }
          const name = decodeURIComponent(params.get("name").toString());
          if (!searchParams.has(name)) {
            throw new Error(`Expected query parameter "${name}" not found`);
          }
          return searchParams.getAll(name).map((value) => encodeURIComponent(value));
        }
        case "@status": {
          if ((0, types_1.isRequest)(context)) {
            throw new Error("Cannot obtain @status component for requests");
          }
          return [context.status.toString()];
        }
        default:
          throw new Error(`Unsupported component "${component}"`);
      }
    }
    exports2.deriveComponent = deriveComponent;
    function extractHeader(header, params, { headers }, req) {
      const context = params.has("req") ? req === null || req === void 0 ? void 0 : req.headers : headers;
      if (!context) {
        throw new Error("Missing request in request-response bound component");
      }
      const headerTuple = Object.entries(context).find(([name]) => name.toLowerCase() === header);
      if (!headerTuple) {
        throw new Error(`No header "${header}" found in headers`);
      }
      const values = Array.isArray(headerTuple[1]) ? headerTuple[1] : [headerTuple[1]];
      if (params.has("bs") && (params.has("sf") || params.has("key"))) {
        throw new Error("Cannot have both `bs` and (implicit) `sf` parameters");
      }
      if (params.has("sf") || params.has("key")) {
        const value = values.join(", ");
        const parsed2 = (0, structured_header_1.parseHeader)(value);
        if (params.has("key") && !(parsed2 instanceof structured_header_1.Dictionary)) {
          throw new Error("Unable to parse header as dictionary");
        }
        if (params.has("key")) {
          const key = params.get("key").toString();
          if (!parsed2.has(key)) {
            throw new Error(`Unable to find key "${key}" in structured field`);
          }
          return [parsed2.get(key)];
        }
        return [parsed2.toString()];
      }
      if (params.has("bs")) {
        return [values.map((val) => {
          const encoded = Buffer.from(val.trim().replace(/\n\s*/gm, " "));
          return `:${encoded.toString("base64")}:`;
        }).join(", ")];
      }
      return [values.map((val) => val.trim().replace(/\n\s*/gm, " ")).join(", ")];
    }
    exports2.extractHeader = extractHeader;
    function normaliseParams(params) {
      const map = /* @__PURE__ */ new Map();
      params.forEach((value, key) => {
        if (value instanceof structured_headers_1.ByteSequence) {
          map.set(key, value.toBase64());
        } else if (value instanceof structured_headers_1.Token) {
          map.set(key, value.toString());
        } else {
          map.set(key, value);
        }
      });
      return map;
    }
    function createSignatureBase(config2, res, req) {
      return config2.fields.reduce((base, fieldName) => {
        var _a;
        const [field, params] = (0, structured_headers_1.parseItem)((0, structured_header_1.quoteString)(fieldName));
        const fieldParams = normaliseParams(params);
        const lcFieldName = field.toLowerCase();
        if (lcFieldName !== "@signature-params") {
          let value = null;
          if (config2.componentParser) {
            value = (_a = config2.componentParser(lcFieldName, fieldParams, res, req)) !== null && _a !== void 0 ? _a : null;
          }
          if (value === null) {
            value = field.startsWith("@") ? deriveComponent(lcFieldName, fieldParams, res, req) : extractHeader(lcFieldName, fieldParams, res, req);
          }
          base.push([(0, structured_headers_1.serializeItem)([field, params]), value]);
        }
        return base;
      }, []);
    }
    exports2.createSignatureBase = createSignatureBase;
    function formatSignatureBase(base) {
      return base.map(([key, value]) => {
        const quotedKey = (0, structured_headers_1.serializeItem)((0, structured_headers_1.parseItem)((0, structured_header_1.quoteString)(key)));
        return value.map((val) => `${quotedKey}: ${val}`).join("\n");
      }).join("\n");
    }
    exports2.formatSignatureBase = formatSignatureBase;
    function createSigningParameters(config2) {
      var _a;
      const now = /* @__PURE__ */ new Date();
      return ((_a = config2.params) !== null && _a !== void 0 ? _a : types_1.defaultParams).reduce((params, paramName) => {
        var _a2, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p, _q, _r, _s;
        let value = "";
        switch (paramName.toLowerCase()) {
          case "created":
            if (((_a2 = config2.paramValues) === null || _a2 === void 0 ? void 0 : _a2.created) !== null) {
              const created = (_c = (_b = config2.paramValues) === null || _b === void 0 ? void 0 : _b.created) !== null && _c !== void 0 ? _c : now;
              value = Math.floor(created.getTime() / 1e3);
            }
            break;
          case "expires":
            if (((_d = config2.paramValues) === null || _d === void 0 ? void 0 : _d.expires) || ((_e = config2.paramValues) === null || _e === void 0 ? void 0 : _e.created) !== null) {
              const expires = (_g = (_f = config2.paramValues) === null || _f === void 0 ? void 0 : _f.expires) !== null && _g !== void 0 ? _g : new Date(((_j = (_h = config2.paramValues) === null || _h === void 0 ? void 0 : _h.created) !== null && _j !== void 0 ? _j : now).getTime() + 3e5);
              value = Math.floor(expires.getTime() / 1e3);
            }
            break;
          case "keyid": {
            const kid = (_m = (_l = (_k = config2.paramValues) === null || _k === void 0 ? void 0 : _k.keyid) !== null && _l !== void 0 ? _l : config2.key.id) !== null && _m !== void 0 ? _m : null;
            if (kid) {
              value = kid.toString();
            }
            break;
          }
          case "alg": {
            const alg = (_q = (_p = (_o = config2.paramValues) === null || _o === void 0 ? void 0 : _o.alg) !== null && _p !== void 0 ? _p : config2.key.alg) !== null && _q !== void 0 ? _q : null;
            if (alg) {
              value = alg.toString();
            }
            break;
          }
          default:
            if (((_r = config2.paramValues) === null || _r === void 0 ? void 0 : _r[paramName]) instanceof Date) {
              value = Math.floor(config2.paramValues[paramName].getTime() / 1e3);
            } else if ((_s = config2.paramValues) === null || _s === void 0 ? void 0 : _s[paramName]) {
              value = config2.paramValues[paramName];
            }
        }
        if (value) {
          params.set(paramName, value);
        }
        return params;
      }, /* @__PURE__ */ new Map());
    }
    exports2.createSigningParameters = createSigningParameters;
    function augmentHeaders(headers, signature, signatureInput, name) {
      let signatureHeaderName = "Signature";
      let signatureInputHeaderName = "Signature-Input";
      let signatureHeader = /* @__PURE__ */ new Map();
      let inputHeader = /* @__PURE__ */ new Map();
      for (const header in headers) {
        switch (header.toLowerCase()) {
          case "signature": {
            signatureHeaderName = header;
            signatureHeader = (0, structured_headers_1.parseDictionary)(Array.isArray(headers[header]) ? headers[header].join(", ") : headers[header]);
            break;
          }
          case "signature-input":
            signatureInputHeaderName = header;
            inputHeader = (0, structured_headers_1.parseDictionary)(Array.isArray(headers[header]) ? headers[header].join(", ") : headers[header]);
            break;
        }
      }
      let signatureName = name !== null && name !== void 0 ? name : "sig";
      if (signatureHeader.has(signatureName) || inputHeader.has(signatureName)) {
        let count = 0;
        while (signatureHeader.has(`${signatureName}${count}`) || inputHeader.has(`${signatureName}${count}`)) {
          count++;
        }
        signatureName += count.toString();
      }
      signatureHeader.set(signatureName, [new structured_headers_1.ByteSequence(signature.toString("base64")), /* @__PURE__ */ new Map()]);
      inputHeader.set(signatureName, (0, structured_headers_1.parseList)(signatureInput)[0]);
      return {
        ...headers,
        [signatureHeaderName]: (0, structured_headers_1.serializeDictionary)(signatureHeader),
        [signatureInputHeaderName]: (0, structured_headers_1.serializeDictionary)(inputHeader)
      };
    }
    exports2.augmentHeaders = augmentHeaders;
    async function signMessage(config2, message, req) {
      var _a;
      const signingParameters = createSigningParameters(config2);
      const signatureBase = createSignatureBase({
        fields: (_a = config2.fields) !== null && _a !== void 0 ? _a : [],
        componentParser: config2.componentParser
      }, message, req);
      const signatureInput = (0, structured_headers_1.serializeList)([
        [
          signatureBase.map(([item]) => (0, structured_headers_1.parseItem)(item)),
          signingParameters
        ]
      ]);
      signatureBase.push(['"@signature-params"', [signatureInput]]);
      const base = formatSignatureBase(signatureBase);
      const signature = await config2.key.sign(Buffer.from(base));
      return {
        ...message,
        headers: augmentHeaders({ ...message.headers }, signature, signatureInput, config2.name)
      };
    }
    exports2.signMessage = signMessage;
    async function verifyMessage(config2, message, req) {
      var _a, _b, _c, _d, _e;
      const { signatures, signatureInputs } = Object.entries(message.headers).reduce((accum, [name, value]) => {
        switch (name.toLowerCase()) {
          case "signature":
            return Object.assign(accum, {
              signatures: (0, structured_headers_1.parseDictionary)(Array.isArray(value) ? value.join(", ") : value)
            });
          case "signature-input":
            return Object.assign(accum, {
              signatureInputs: (0, structured_headers_1.parseDictionary)(Array.isArray(value) ? value.join(", ") : value)
            });
          default:
            return accum;
        }
      }, {});
      if (!(signatures === null || signatures === void 0 ? void 0 : signatures.size) && !(signatureInputs === null || signatureInputs === void 0 ? void 0 : signatureInputs.size)) {
        return null;
      }
      if (!(signatures === null || signatures === void 0 ? void 0 : signatures.size) || !(signatureInputs === null || signatureInputs === void 0 ? void 0 : signatureInputs.size)) {
        throw new Error("Incomplete signature headers");
      }
      const now = Math.floor(Date.now() / 1e3);
      const tolerance = (_a = config2.tolerance) !== null && _a !== void 0 ? _a : 0;
      const notAfter = config2.notAfter instanceof Date ? Math.floor(config2.notAfter.getTime() / 1e3) : (_b = config2.notAfter) !== null && _b !== void 0 ? _b : now;
      const maxAge = (_c = config2.maxAge) !== null && _c !== void 0 ? _c : null;
      const requiredParams = (_d = config2.requiredParams) !== null && _d !== void 0 ? _d : [];
      const requiredFields = (_e = config2.requiredFields) !== null && _e !== void 0 ? _e : [];
      return Array.from(signatureInputs.entries()).reduce(async (prev, [name, input]) => {
        var _a2;
        const signatureParams = Array.from(input[1].entries()).reduce((params, [key2, value]) => {
          if (value instanceof structured_headers_1.ByteSequence) {
            Object.assign(params, {
              [key2]: value.toBase64()
            });
          } else if (value instanceof structured_headers_1.Token) {
            Object.assign(params, {
              [key2]: value.toString()
            });
          } else if (key2 === "created" || key2 === "expired") {
            Object.assign(params, {
              [key2]: new Date(value * 1e3)
            });
          } else {
            Object.assign(params, {
              [key2]: value
            });
          }
          return params;
        }, {});
        const [result, key] = await Promise.all([
          prev.catch((e) => e),
          config2.keyLookup(signatureParams)
        ]);
        if (config2.all && !key) {
          throw new errors_1.UnknownKeyError("Unknown key");
        }
        if (!key) {
          if (result instanceof Error) {
            throw result;
          }
          return result;
        }
        if (input[1].has("alg") && ((_a2 = key.algs) === null || _a2 === void 0 ? void 0 : _a2.includes(input[1].get("alg"))) === false) {
          throw new errors_1.UnsupportedAlgorithmError("Unsupported key algorithm");
        }
        if (!(0, structured_headers_1.isInnerList)(input)) {
          throw new errors_1.MalformedSignatureError("Malformed signature input");
        }
        const hasRequiredParams = requiredParams.every((param) => input[1].has(param));
        if (!hasRequiredParams) {
          throw new errors_1.UnacceptableSignatureError("Missing required signature parameters");
        }
        const hasRequiredFields = requiredFields.every((field) => input[0].some(([fieldName]) => fieldName === field));
        if (!hasRequiredFields) {
          throw new errors_1.UnacceptableSignatureError("Missing required signed fields");
        }
        if (input[1].has("created")) {
          const created = input[1].get("created") - tolerance;
          if (maxAge && now - created > maxAge || created > notAfter) {
            throw new errors_1.ExpiredError("Signature is too old");
          }
        }
        if (input[1].has("expires")) {
          const expires = input[1].get("expires") + tolerance;
          if (now > expires) {
            throw new errors_1.ExpiredError("Signature has expired");
          }
        }
        const fields = input[0].map((item) => (0, structured_headers_1.serializeItem)(item));
        const signingBase = createSignatureBase({ fields, componentParser: config2.componentParser }, message, req);
        signingBase.push(['"@signature-params"', [(0, structured_headers_1.serializeList)([input])]]);
        const base = formatSignatureBase(signingBase);
        const signature = signatures.get(name);
        if (!signature) {
          throw new errors_1.MalformedSignatureError("No corresponding signature for input");
        }
        if (!(0, structured_headers_1.isByteSequence)(signature[0])) {
          throw new errors_1.MalformedSignatureError("Malformed signature");
        }
        return key.verify(Buffer.from(base), Buffer.from(signature[0].toBase64(), "base64"), signatureParams);
      }, Promise.resolve(null));
    }
    exports2.verifyMessage = verifyMessage;
  }
});

// node_modules/http-message-signatures/lib/cavage/index.js
var require_cavage = __commonJS({
  "node_modules/http-message-signatures/lib/cavage/index.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.verifyMessage = exports2.signMessage = exports2.createSignatureBase = exports2.createSigningParameters = exports2.formatSignatureBase = exports2.extractHeader = exports2.deriveComponent = void 0;
    var structured_headers_1 = require_dist();
    var types_1 = require_types();
    var structured_header_1 = require_structured_header();
    function mapCavageAlgorithm(alg) {
      switch (alg.toLowerCase()) {
        case "hs2019":
          return "rsa-pss-sha512";
        case "rsa-sha1":
          return "rsa-v1_5-sha1";
        case "rsa-sha256":
          return "rsa-v1_5-sha256";
        case "ecdsa-sha256":
          return "ecdsa-p256-sha256";
        default:
          return alg;
      }
    }
    function mapHttpbisAlgorithm(alg) {
      switch (alg.toLowerCase()) {
        case "rsa-pss-sha512":
          return "hs2019";
        case "rsa-v1_5-sha1":
          return "rsa-sha1";
        case "rsa-v1_5-sha256":
          return "rsa-sha256";
        case "ecdsa-p256-sha256":
          return "ecdsa-sha256";
        default:
          return alg;
      }
    }
    function deriveComponent(component, message) {
      const [componentName, params] = (0, structured_headers_1.parseItem)((0, structured_header_1.quoteString)(component));
      if (params.size) {
        throw new Error("Component parameters are not supported in cavage");
      }
      switch (componentName.toString().toLowerCase()) {
        case "@request-target": {
          if (!(0, types_1.isRequest)(message)) {
            throw new Error("Cannot derive @request-target on response");
          }
          const { pathname, search } = typeof message.url === "string" ? new URL(message.url) : message.url;
          return [`${message.method.toLowerCase()} ${pathname}${search}`];
        }
        default:
          throw new Error(`Unsupported component "${component}"`);
      }
    }
    exports2.deriveComponent = deriveComponent;
    function extractHeader(header, { headers }) {
      const [headerName, params] = (0, structured_headers_1.parseItem)((0, structured_header_1.quoteString)(header));
      if (params.size) {
        throw new Error("Field parameters are not supported in cavage");
      }
      const lcHeaderName = headerName.toString().toLowerCase();
      const headerTuple = Object.entries(headers).find(([name]) => name.toLowerCase() === lcHeaderName);
      if (!headerTuple) {
        throw new Error(`No header ${headerName} found in headers`);
      }
      return [(Array.isArray(headerTuple[1]) ? headerTuple[1] : [headerTuple[1]]).map((val) => val.trim().replace(/\n\s*/gm, " ")).join(", ")];
    }
    exports2.extractHeader = extractHeader;
    function formatSignatureBase(base) {
      return base.reduce((accum, [key, value]) => {
        const [keyName] = (0, structured_headers_1.parseItem)((0, structured_header_1.quoteString)(key));
        const lcKey = keyName.toLowerCase();
        if (lcKey.startsWith("@")) {
          accum.push(`(${lcKey.slice(1)}): ${value.join(", ")}`);
        } else {
          accum.push(`${key.toLowerCase()}: ${value.join(", ")}`);
        }
        return accum;
      }, []).join("\n");
    }
    exports2.formatSignatureBase = formatSignatureBase;
    function createSigningParameters(config2) {
      var _a;
      const now = /* @__PURE__ */ new Date();
      return ((_a = config2.params) !== null && _a !== void 0 ? _a : types_1.defaultParams).reduce((params, paramName) => {
        var _a2, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p, _q, _r, _s;
        let value = "";
        switch (paramName.toLowerCase()) {
          case "created":
            if (((_a2 = config2.paramValues) === null || _a2 === void 0 ? void 0 : _a2.created) !== null) {
              const created = (_c = (_b = config2.paramValues) === null || _b === void 0 ? void 0 : _b.created) !== null && _c !== void 0 ? _c : now;
              value = Math.floor(created.getTime() / 1e3);
            }
            break;
          case "expires":
            if (((_d = config2.paramValues) === null || _d === void 0 ? void 0 : _d.expires) || ((_e = config2.paramValues) === null || _e === void 0 ? void 0 : _e.created) !== null) {
              const expires = (_g = (_f = config2.paramValues) === null || _f === void 0 ? void 0 : _f.expires) !== null && _g !== void 0 ? _g : new Date(((_j = (_h = config2.paramValues) === null || _h === void 0 ? void 0 : _h.created) !== null && _j !== void 0 ? _j : now).getTime() + 3e5);
              value = Math.floor(expires.getTime() / 1e3);
            }
            break;
          case "keyid": {
            const kid = (_m = (_l = (_k = config2.paramValues) === null || _k === void 0 ? void 0 : _k.keyid) !== null && _l !== void 0 ? _l : config2.key.id) !== null && _m !== void 0 ? _m : null;
            if (kid) {
              value = kid.toString();
            }
            break;
          }
          case "alg": {
            const alg = (_q = (_p = (_o = config2.paramValues) === null || _o === void 0 ? void 0 : _o.alg) !== null && _p !== void 0 ? _p : config2.key.alg) !== null && _q !== void 0 ? _q : null;
            if (alg) {
              value = alg.toString();
            }
            break;
          }
          default:
            if (((_r = config2.paramValues) === null || _r === void 0 ? void 0 : _r[paramName]) instanceof Date) {
              value = Math.floor(config2.paramValues[paramName].getTime() / 1e3).toString();
            } else if ((_s = config2.paramValues) === null || _s === void 0 ? void 0 : _s[paramName]) {
              value = config2.paramValues[paramName];
            }
        }
        if (value) {
          params.set(paramName, value);
        }
        return params;
      }, /* @__PURE__ */ new Map());
    }
    exports2.createSigningParameters = createSigningParameters;
    function createSignatureBase(fields, message, signingParameters) {
      return fields.reduce((base, fieldName) => {
        const [field, params] = (0, structured_headers_1.parseItem)((0, structured_header_1.quoteString)(fieldName));
        if (params.size) {
          throw new Error("Field parameters are not supported");
        }
        const lcFieldName = field.toString().toLowerCase();
        switch (lcFieldName) {
          case "@created":
            if (signingParameters.has("created")) {
              base.push(["(created)", [signingParameters.get("created")]]);
            }
            break;
          case "@expires":
            if (signingParameters.has("expires")) {
              base.push(["(expires)", [signingParameters.get("expires")]]);
            }
            break;
          case "@request-target": {
            if (!(0, types_1.isRequest)(message)) {
              throw new Error("Cannot read target of response");
            }
            const { pathname, search } = typeof message.url === "string" ? new URL(message.url) : message.url;
            base.push(["(request-target)", [`${message.method.toLowerCase()} ${pathname}${search}`]]);
            break;
          }
          default:
            base.push([lcFieldName, extractHeader(lcFieldName, message)]);
        }
        return base;
      }, []);
    }
    exports2.createSignatureBase = createSignatureBase;
    async function signMessage(config2, message) {
      var _a;
      const signingParameters = createSigningParameters(config2);
      const signatureBase = createSignatureBase((_a = config2.fields) !== null && _a !== void 0 ? _a : ["@created"], message, signingParameters);
      const base = formatSignatureBase(signatureBase);
      const signature = await config2.key.sign(Buffer.from(base));
      const headerNames = signatureBase.map(([key]) => key);
      const header = [
        ...Array.from(signingParameters.entries()).map(([name, value]) => {
          if (name === "alg") {
            return `algorithm="${mapHttpbisAlgorithm(value)}"`;
          }
          if (name === "keyid") {
            return `keyId="${value}"`;
          }
          if (typeof value === "number") {
            return `${name}=${value}`;
          }
          return `${name}="${value.toString()}"`;
        }),
        `headers="${headerNames.join(" ")}"`,
        `signature="${signature.toString("base64")}"`
      ].join(",");
      return {
        ...message,
        headers: {
          ...message.headers,
          Signature: header
        }
      };
    }
    exports2.signMessage = signMessage;
    async function verifyMessage(config2, message) {
      var _a, _b, _c, _d, _e, _f, _g;
      const header = Object.entries(message.headers).find(([name]) => name.toLowerCase() === "signature");
      if (!header) {
        return null;
      }
      const parsedHeader = (Array.isArray(header[1]) ? header[1].join(", ") : header[1]).split(",").reduce((parts, value) => {
        const [key2, ...values] = value.trim().split("=");
        if (parts.has(key2)) {
          throw new Error("Same parameter defined repeatedly");
        }
        const val = values.join("=").replace(/^"(.*)"$/, "$1");
        switch (key2.toLowerCase()) {
          case "created":
          case "expires":
            parts.set(key2, parseInt(val, 10));
            break;
          default:
            parts.set(key2, val);
        }
        return parts;
      }, /* @__PURE__ */ new Map());
      if (!parsedHeader.has("signature")) {
        throw new Error("Missing signature from header");
      }
      const baseParts = new Map(createSignatureBase(((_a = parsedHeader.get("headers")) !== null && _a !== void 0 ? _a : "(created)").split(" ").map((component) => {
        return component.toLowerCase().replace(/^\((.*)\)$/, "@$1");
      }), message, parsedHeader));
      const base = formatSignatureBase(Array.from(baseParts.entries()));
      const now = Math.floor(Date.now() / 1e3);
      const tolerance = (_b = config2.tolerance) !== null && _b !== void 0 ? _b : 0;
      const notAfter = config2.notAfter instanceof Date ? Math.floor(config2.notAfter.getTime() / 1e3) : (_c = config2.notAfter) !== null && _c !== void 0 ? _c : now;
      const maxAge = (_d = config2.maxAge) !== null && _d !== void 0 ? _d : null;
      const requiredParams = (_e = config2.requiredParams) !== null && _e !== void 0 ? _e : [];
      const requiredFields = (_f = config2.requiredFields) !== null && _f !== void 0 ? _f : [];
      const hasRequiredParams = requiredParams.every((param) => baseParts.has(param));
      if (!hasRequiredParams) {
        return false;
      }
      const hasRequiredFields = requiredFields.every((field) => {
        return parsedHeader.has(field.toLowerCase().replace(/^@(.*)/, "($1)"));
      });
      if (!hasRequiredFields) {
        return false;
      }
      if (parsedHeader.has("created")) {
        const created = parsedHeader.get("created") - tolerance;
        if (maxAge && created - now > maxAge) {
          return false;
        }
        if (created > notAfter) {
          return false;
        }
      }
      if (parsedHeader.has("expires")) {
        const expires = parsedHeader.get("expires") + tolerance;
        if (expires > now) {
          return false;
        }
      }
      const params = Array.from(parsedHeader.entries()).reduce((params2, [key2, value]) => {
        let keyName = key2;
        let val;
        switch (key2.toLowerCase()) {
          case "created":
          case "expires":
            val = new Date(value * 1e3);
            break;
          case "signature":
          case "headers":
            return params2;
          case "algorithm":
            keyName = "alg";
            val = mapCavageAlgorithm(value);
            break;
          case "keyid":
            keyName = "keyid";
            val = value;
            break;
          default: {
            if (typeof value === "string" || typeof value === "number") {
              val = value;
            } else {
              val = value.toString();
            }
          }
        }
        return Object.assign(params2, {
          [keyName]: val
        });
      }, {});
      const key = await config2.keyLookup(params);
      return (_g = key === null || key === void 0 ? void 0 : key.verify(Buffer.from(base), Buffer.from(parsedHeader.get("signature"), "base64"), params)) !== null && _g !== void 0 ? _g : null;
    }
    exports2.verifyMessage = verifyMessage;
  }
});

// node_modules/http-message-signatures/lib/index.js
var require_lib = __commonJS({
  "node_modules/http-message-signatures/lib/index.js"(exports2) {
    "use strict";
    var __createBinding = exports2 && exports2.__createBinding || (Object.create ? (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      var desc = Object.getOwnPropertyDescriptor(m, k);
      if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
        desc = { enumerable: true, get: function() {
          return m[k];
        } };
      }
      Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    }));
    var __setModuleDefault = exports2 && exports2.__setModuleDefault || (Object.create ? (function(o, v) {
      Object.defineProperty(o, "default", { enumerable: true, value: v });
    }) : function(o, v) {
      o["default"] = v;
    });
    var __exportStar = exports2 && exports2.__exportStar || function(m, exports3) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports3, p)) __createBinding(exports3, m, p);
    };
    var __importStar = exports2 && exports2.__importStar || function(mod) {
      if (mod && mod.__esModule) return mod;
      var result = {};
      if (mod != null) {
        for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
      }
      __setModuleDefault(result, mod);
      return result;
    };
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.cavage = exports2.httpbis = exports2.default = void 0;
    __exportStar(require_algorithm(), exports2);
    __exportStar(require_types(), exports2);
    __exportStar(require_errors(), exports2);
    exports2.default = __importStar(require_httpbis());
    exports2.httpbis = __importStar(require_httpbis());
    exports2.cavage = __importStar(require_cavage());
  }
});

// node_modules/dotenv/package.json
var require_package = __commonJS({
  "node_modules/dotenv/package.json"(exports2, module2) {
    module2.exports = {
      name: "dotenv",
      version: "17.3.1",
      description: "Loads environment variables from .env file",
      main: "lib/main.js",
      types: "lib/main.d.ts",
      exports: {
        ".": {
          types: "./lib/main.d.ts",
          require: "./lib/main.js",
          default: "./lib/main.js"
        },
        "./config": "./config.js",
        "./config.js": "./config.js",
        "./lib/env-options": "./lib/env-options.js",
        "./lib/env-options.js": "./lib/env-options.js",
        "./lib/cli-options": "./lib/cli-options.js",
        "./lib/cli-options.js": "./lib/cli-options.js",
        "./package.json": "./package.json"
      },
      scripts: {
        "dts-check": "tsc --project tests/types/tsconfig.json",
        lint: "standard",
        pretest: "npm run lint && npm run dts-check",
        test: "tap run tests/**/*.js --allow-empty-coverage --disable-coverage --timeout=60000",
        "test:coverage": "tap run tests/**/*.js --show-full-coverage --timeout=60000 --coverage-report=text --coverage-report=lcov",
        prerelease: "npm test",
        release: "standard-version"
      },
      repository: {
        type: "git",
        url: "git://github.com/motdotla/dotenv.git"
      },
      homepage: "https://github.com/motdotla/dotenv#readme",
      funding: "https://dotenvx.com",
      keywords: [
        "dotenv",
        "env",
        ".env",
        "environment",
        "variables",
        "config",
        "settings"
      ],
      readmeFilename: "README.md",
      license: "BSD-2-Clause",
      devDependencies: {
        "@types/node": "^18.11.3",
        decache: "^4.6.2",
        sinon: "^14.0.1",
        standard: "^17.0.0",
        "standard-version": "^9.5.0",
        tap: "^19.2.0",
        typescript: "^4.8.4"
      },
      engines: {
        node: ">=12"
      },
      browser: {
        fs: false
      }
    };
  }
});

// node_modules/dotenv/lib/main.js
var require_main = __commonJS({
  "node_modules/dotenv/lib/main.js"(exports2, module2) {
    var fs7 = require("fs");
    var path5 = require("path");
    var os4 = require("os");
    var crypto = require("crypto");
    var packageJson = require_package();
    var version = packageJson.version;
    var TIPS = [
      "\u{1F510} encrypt with Dotenvx: https://dotenvx.com",
      "\u{1F510} prevent committing .env to code: https://dotenvx.com/precommit",
      "\u{1F510} prevent building .env in docker: https://dotenvx.com/prebuild",
      "\u{1F916} agentic secret storage: https://dotenvx.com/as2",
      "\u26A1\uFE0F secrets for agents: https://dotenvx.com/as2",
      "\u{1F6E1}\uFE0F auth for agents: https://vestauth.com",
      "\u{1F6E0}\uFE0F  run anywhere with `dotenvx run -- yourcommand`",
      "\u2699\uFE0F  specify custom .env file path with { path: '/custom/path/.env' }",
      "\u2699\uFE0F  enable debug logging with { debug: true }",
      "\u2699\uFE0F  override existing env vars with { override: true }",
      "\u2699\uFE0F  suppress all logs with { quiet: true }",
      "\u2699\uFE0F  write to custom object with { processEnv: myObject }",
      "\u2699\uFE0F  load multiple .env files with { path: ['.env.local', '.env'] }"
    ];
    function _getRandomTip() {
      return TIPS[Math.floor(Math.random() * TIPS.length)];
    }
    function parseBoolean(value) {
      if (typeof value === "string") {
        return !["false", "0", "no", "off", ""].includes(value.toLowerCase());
      }
      return Boolean(value);
    }
    function supportsAnsi() {
      return process.stdout.isTTY;
    }
    function dim(text) {
      return supportsAnsi() ? `\x1B[2m${text}\x1B[0m` : text;
    }
    var LINE = /(?:^|^)\s*(?:export\s+)?([\w.-]+)(?:\s*=\s*?|:\s+?)(\s*'(?:\\'|[^'])*'|\s*"(?:\\"|[^"])*"|\s*`(?:\\`|[^`])*`|[^#\r\n]+)?\s*(?:#.*)?(?:$|$)/mg;
    function parse(src) {
      const obj = {};
      let lines = src.toString();
      lines = lines.replace(/\r\n?/mg, "\n");
      let match;
      while ((match = LINE.exec(lines)) != null) {
        const key = match[1];
        let value = match[2] || "";
        value = value.trim();
        const maybeQuote = value[0];
        value = value.replace(/^(['"`])([\s\S]*)\1$/mg, "$2");
        if (maybeQuote === '"') {
          value = value.replace(/\\n/g, "\n");
          value = value.replace(/\\r/g, "\r");
        }
        obj[key] = value;
      }
      return obj;
    }
    function _parseVault(options) {
      options = options || {};
      const vaultPath = _vaultPath(options);
      options.path = vaultPath;
      const result = DotenvModule.configDotenv(options);
      if (!result.parsed) {
        const err = new Error(`MISSING_DATA: Cannot parse ${vaultPath} for an unknown reason`);
        err.code = "MISSING_DATA";
        throw err;
      }
      const keys = _dotenvKey(options).split(",");
      const length = keys.length;
      let decrypted;
      for (let i = 0; i < length; i++) {
        try {
          const key = keys[i].trim();
          const attrs = _instructions(result, key);
          decrypted = DotenvModule.decrypt(attrs.ciphertext, attrs.key);
          break;
        } catch (error) {
          if (i + 1 >= length) {
            throw error;
          }
        }
      }
      return DotenvModule.parse(decrypted);
    }
    function _warn(message) {
      console.error(`[dotenv@${version}][WARN] ${message}`);
    }
    function _debug(message) {
      console.log(`[dotenv@${version}][DEBUG] ${message}`);
    }
    function _log(message) {
      console.log(`[dotenv@${version}] ${message}`);
    }
    function _dotenvKey(options) {
      if (options && options.DOTENV_KEY && options.DOTENV_KEY.length > 0) {
        return options.DOTENV_KEY;
      }
      if (process.env.DOTENV_KEY && process.env.DOTENV_KEY.length > 0) {
        return process.env.DOTENV_KEY;
      }
      return "";
    }
    function _instructions(result, dotenvKey) {
      let uri;
      try {
        uri = new URL(dotenvKey);
      } catch (error) {
        if (error.code === "ERR_INVALID_URL") {
          const err = new Error("INVALID_DOTENV_KEY: Wrong format. Must be in valid uri format like dotenv://:key_1234@dotenvx.com/vault/.env.vault?environment=development");
          err.code = "INVALID_DOTENV_KEY";
          throw err;
        }
        throw error;
      }
      const key = uri.password;
      if (!key) {
        const err = new Error("INVALID_DOTENV_KEY: Missing key part");
        err.code = "INVALID_DOTENV_KEY";
        throw err;
      }
      const environment = uri.searchParams.get("environment");
      if (!environment) {
        const err = new Error("INVALID_DOTENV_KEY: Missing environment part");
        err.code = "INVALID_DOTENV_KEY";
        throw err;
      }
      const environmentKey = `DOTENV_VAULT_${environment.toUpperCase()}`;
      const ciphertext = result.parsed[environmentKey];
      if (!ciphertext) {
        const err = new Error(`NOT_FOUND_DOTENV_ENVIRONMENT: Cannot locate environment ${environmentKey} in your .env.vault file.`);
        err.code = "NOT_FOUND_DOTENV_ENVIRONMENT";
        throw err;
      }
      return { ciphertext, key };
    }
    function _vaultPath(options) {
      let possibleVaultPath = null;
      if (options && options.path && options.path.length > 0) {
        if (Array.isArray(options.path)) {
          for (const filepath of options.path) {
            if (fs7.existsSync(filepath)) {
              possibleVaultPath = filepath.endsWith(".vault") ? filepath : `${filepath}.vault`;
            }
          }
        } else {
          possibleVaultPath = options.path.endsWith(".vault") ? options.path : `${options.path}.vault`;
        }
      } else {
        possibleVaultPath = path5.resolve(process.cwd(), ".env.vault");
      }
      if (fs7.existsSync(possibleVaultPath)) {
        return possibleVaultPath;
      }
      return null;
    }
    function _resolveHome(envPath) {
      return envPath[0] === "~" ? path5.join(os4.homedir(), envPath.slice(1)) : envPath;
    }
    function _configVault(options) {
      const debug = parseBoolean(process.env.DOTENV_CONFIG_DEBUG || options && options.debug);
      const quiet = parseBoolean(process.env.DOTENV_CONFIG_QUIET || options && options.quiet);
      if (debug || !quiet) {
        _log("Loading env from encrypted .env.vault");
      }
      const parsed2 = DotenvModule._parseVault(options);
      let processEnv = process.env;
      if (options && options.processEnv != null) {
        processEnv = options.processEnv;
      }
      DotenvModule.populate(processEnv, parsed2, options);
      return { parsed: parsed2 };
    }
    function configDotenv(options) {
      const dotenvPath = path5.resolve(process.cwd(), ".env");
      let encoding = "utf8";
      let processEnv = process.env;
      if (options && options.processEnv != null) {
        processEnv = options.processEnv;
      }
      let debug = parseBoolean(processEnv.DOTENV_CONFIG_DEBUG || options && options.debug);
      let quiet = parseBoolean(processEnv.DOTENV_CONFIG_QUIET || options && options.quiet);
      if (options && options.encoding) {
        encoding = options.encoding;
      } else {
        if (debug) {
          _debug("No encoding is specified. UTF-8 is used by default");
        }
      }
      let optionPaths = [dotenvPath];
      if (options && options.path) {
        if (!Array.isArray(options.path)) {
          optionPaths = [_resolveHome(options.path)];
        } else {
          optionPaths = [];
          for (const filepath of options.path) {
            optionPaths.push(_resolveHome(filepath));
          }
        }
      }
      let lastError;
      const parsedAll = {};
      for (const path6 of optionPaths) {
        try {
          const parsed2 = DotenvModule.parse(fs7.readFileSync(path6, { encoding }));
          DotenvModule.populate(parsedAll, parsed2, options);
        } catch (e) {
          if (debug) {
            _debug(`Failed to load ${path6} ${e.message}`);
          }
          lastError = e;
        }
      }
      const populated = DotenvModule.populate(processEnv, parsedAll, options);
      debug = parseBoolean(processEnv.DOTENV_CONFIG_DEBUG || debug);
      quiet = parseBoolean(processEnv.DOTENV_CONFIG_QUIET || quiet);
      if (debug || !quiet) {
        const keysCount = Object.keys(populated).length;
        const shortPaths = [];
        for (const filePath of optionPaths) {
          try {
            const relative = path5.relative(process.cwd(), filePath);
            shortPaths.push(relative);
          } catch (e) {
            if (debug) {
              _debug(`Failed to load ${filePath} ${e.message}`);
            }
            lastError = e;
          }
        }
        _log(`injecting env (${keysCount}) from ${shortPaths.join(",")} ${dim(`-- tip: ${_getRandomTip()}`)}`);
      }
      if (lastError) {
        return { parsed: parsedAll, error: lastError };
      } else {
        return { parsed: parsedAll };
      }
    }
    function config2(options) {
      if (_dotenvKey(options).length === 0) {
        return DotenvModule.configDotenv(options);
      }
      const vaultPath = _vaultPath(options);
      if (!vaultPath) {
        _warn(`You set DOTENV_KEY but you are missing a .env.vault file at ${vaultPath}. Did you forget to build it?`);
        return DotenvModule.configDotenv(options);
      }
      return DotenvModule._configVault(options);
    }
    function decrypt(encrypted, keyStr) {
      const key = Buffer.from(keyStr.slice(-64), "hex");
      let ciphertext = Buffer.from(encrypted, "base64");
      const nonce = ciphertext.subarray(0, 12);
      const authTag = ciphertext.subarray(-16);
      ciphertext = ciphertext.subarray(12, -16);
      try {
        const aesgcm = crypto.createDecipheriv("aes-256-gcm", key, nonce);
        aesgcm.setAuthTag(authTag);
        return `${aesgcm.update(ciphertext)}${aesgcm.final()}`;
      } catch (error) {
        const isRange = error instanceof RangeError;
        const invalidKeyLength = error.message === "Invalid key length";
        const decryptionFailed = error.message === "Unsupported state or unable to authenticate data";
        if (isRange || invalidKeyLength) {
          const err = new Error("INVALID_DOTENV_KEY: It must be 64 characters long (or more)");
          err.code = "INVALID_DOTENV_KEY";
          throw err;
        } else if (decryptionFailed) {
          const err = new Error("DECRYPTION_FAILED: Please check your DOTENV_KEY");
          err.code = "DECRYPTION_FAILED";
          throw err;
        } else {
          throw error;
        }
      }
    }
    function populate(processEnv, parsed2, options = {}) {
      const debug = Boolean(options && options.debug);
      const override = Boolean(options && options.override);
      const populated = {};
      if (typeof parsed2 !== "object") {
        const err = new Error("OBJECT_REQUIRED: Please check the processEnv argument being passed to populate");
        err.code = "OBJECT_REQUIRED";
        throw err;
      }
      for (const key of Object.keys(parsed2)) {
        if (Object.prototype.hasOwnProperty.call(processEnv, key)) {
          if (override === true) {
            processEnv[key] = parsed2[key];
            populated[key] = parsed2[key];
          }
          if (debug) {
            if (override === true) {
              _debug(`"${key}" is already defined and WAS overwritten`);
            } else {
              _debug(`"${key}" is already defined and was NOT overwritten`);
            }
          }
        } else {
          processEnv[key] = parsed2[key];
          populated[key] = parsed2[key];
        }
      }
      return populated;
    }
    var DotenvModule = {
      configDotenv,
      _configVault,
      _parseVault,
      config: config2,
      decrypt,
      parse,
      populate
    };
    module2.exports.configDotenv = DotenvModule.configDotenv;
    module2.exports._configVault = DotenvModule._configVault;
    module2.exports._parseVault = DotenvModule._parseVault;
    module2.exports.config = DotenvModule.config;
    module2.exports.decrypt = DotenvModule.decrypt;
    module2.exports.parse = DotenvModule.parse;
    module2.exports.populate = DotenvModule.populate;
    module2.exports = DotenvModule;
  }
});

// node_modules/commander/esm.mjs
var import_index = __toESM(require_commander(), 1);
var {
  program,
  createCommand,
  createArgument,
  createOption,
  CommanderError,
  InvalidArgumentError,
  InvalidOptionArgumentError,
  // deprecated old name
  Command,
  Argument,
  Option,
  Help
} = import_index.default;

// node_modules/open/index.js
var import_node_process7 = __toESM(require("node:process"), 1);
var import_node_path = __toESM(require("node:path"), 1);
var import_node_url = require("node:url");
var import_node_child_process7 = __toESM(require("node:child_process"), 1);
var import_promises2 = __toESM(require("node:fs/promises"), 1);

// node_modules/wsl-utils/index.js
var import_node_util2 = require("node:util");
var import_node_child_process2 = __toESM(require("node:child_process"), 1);
var import_promises = __toESM(require("node:fs/promises"), 1);

// node_modules/is-wsl/index.js
var import_node_process = __toESM(require("node:process"), 1);
var import_node_os = __toESM(require("node:os"), 1);
var import_node_fs3 = __toESM(require("node:fs"), 1);

// node_modules/is-inside-container/index.js
var import_node_fs2 = __toESM(require("node:fs"), 1);

// node_modules/is-docker/index.js
var import_node_fs = __toESM(require("node:fs"), 1);
var isDockerCached;
function hasDockerEnv() {
  try {
    import_node_fs.default.statSync("/.dockerenv");
    return true;
  } catch {
    return false;
  }
}
function hasDockerCGroup() {
  try {
    return import_node_fs.default.readFileSync("/proc/self/cgroup", "utf8").includes("docker");
  } catch {
    return false;
  }
}
function isDocker() {
  if (isDockerCached === void 0) {
    isDockerCached = hasDockerEnv() || hasDockerCGroup();
  }
  return isDockerCached;
}

// node_modules/is-inside-container/index.js
var cachedResult;
var hasContainerEnv = () => {
  try {
    import_node_fs2.default.statSync("/run/.containerenv");
    return true;
  } catch {
    return false;
  }
};
function isInsideContainer() {
  if (cachedResult === void 0) {
    cachedResult = hasContainerEnv() || isDocker();
  }
  return cachedResult;
}

// node_modules/is-wsl/index.js
var isWsl = () => {
  if (import_node_process.default.platform !== "linux") {
    return false;
  }
  if (import_node_os.default.release().toLowerCase().includes("microsoft")) {
    if (isInsideContainer()) {
      return false;
    }
    return true;
  }
  try {
    if (import_node_fs3.default.readFileSync("/proc/version", "utf8").toLowerCase().includes("microsoft")) {
      return !isInsideContainer();
    }
  } catch {
  }
  if (import_node_fs3.default.existsSync("/proc/sys/fs/binfmt_misc/WSLInterop") || import_node_fs3.default.existsSync("/run/WSL")) {
    return !isInsideContainer();
  }
  return false;
};
var is_wsl_default = import_node_process.default.env.__IS_WSL_TEST__ ? isWsl : isWsl();

// node_modules/powershell-utils/index.js
var import_node_process2 = __toESM(require("node:process"), 1);
var import_node_buffer = require("node:buffer");
var import_node_util = require("node:util");
var import_node_child_process = __toESM(require("node:child_process"), 1);
var execFile = (0, import_node_util.promisify)(import_node_child_process.default.execFile);
var powerShellPath = () => `${import_node_process2.default.env.SYSTEMROOT || import_node_process2.default.env.windir || String.raw`C:\Windows`}\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`;
var executePowerShell = async (command, options = {}) => {
  const {
    powerShellPath: psPath,
    ...execFileOptions
  } = options;
  const encodedCommand = executePowerShell.encodeCommand(command);
  return execFile(
    psPath ?? powerShellPath(),
    [
      ...executePowerShell.argumentsPrefix,
      encodedCommand
    ],
    {
      encoding: "utf8",
      ...execFileOptions
    }
  );
};
executePowerShell.argumentsPrefix = [
  "-NoProfile",
  "-NonInteractive",
  "-ExecutionPolicy",
  "Bypass",
  "-EncodedCommand"
];
executePowerShell.encodeCommand = (command) => import_node_buffer.Buffer.from(command, "utf16le").toString("base64");
executePowerShell.escapeArgument = (value) => `'${String(value).replaceAll("'", "''")}'`;

// node_modules/wsl-utils/utilities.js
function parseMountPointFromConfig(content) {
  for (const line of content.split("\n")) {
    if (/^\s*#/.test(line)) {
      continue;
    }
    const match = /^\s*root\s*=\s*(?<mountPoint>"[^"]*"|'[^']*'|[^#]*)/.exec(line);
    if (!match) {
      continue;
    }
    return match.groups.mountPoint.trim().replaceAll(/^["']|["']$/g, "");
  }
}

// node_modules/wsl-utils/index.js
var execFile2 = (0, import_node_util2.promisify)(import_node_child_process2.default.execFile);
var wslDrivesMountPoint = /* @__PURE__ */ (() => {
  const defaultMountPoint = "/mnt/";
  let mountPoint;
  return async function() {
    if (mountPoint) {
      return mountPoint;
    }
    const configFilePath = "/etc/wsl.conf";
    let isConfigFileExists = false;
    try {
      await import_promises.default.access(configFilePath, import_promises.constants.F_OK);
      isConfigFileExists = true;
    } catch {
    }
    if (!isConfigFileExists) {
      return defaultMountPoint;
    }
    const configContent = await import_promises.default.readFile(configFilePath, { encoding: "utf8" });
    const parsedMountPoint = parseMountPointFromConfig(configContent);
    if (parsedMountPoint === void 0) {
      return defaultMountPoint;
    }
    mountPoint = parsedMountPoint;
    mountPoint = mountPoint.endsWith("/") ? mountPoint : `${mountPoint}/`;
    return mountPoint;
  };
})();
var powerShellPathFromWsl = async () => {
  const mountPoint = await wslDrivesMountPoint();
  return `${mountPoint}c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`;
};
var powerShellPath2 = is_wsl_default ? powerShellPathFromWsl : powerShellPath;
var canAccessPowerShellPromise;
var canAccessPowerShell = async () => {
  canAccessPowerShellPromise ??= (async () => {
    try {
      const psPath = await powerShellPath2();
      await import_promises.default.access(psPath, import_promises.constants.X_OK);
      return true;
    } catch {
      return false;
    }
  })();
  return canAccessPowerShellPromise;
};
var wslDefaultBrowser = async () => {
  const psPath = await powerShellPath2();
  const command = String.raw`(Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice").ProgId`;
  const { stdout } = await executePowerShell(command, { powerShellPath: psPath });
  return stdout.trim();
};
var convertWslPathToWindows = async (path5) => {
  if (/^[a-z]+:\/\//i.test(path5)) {
    return path5;
  }
  try {
    const { stdout } = await execFile2("wslpath", ["-aw", path5], { encoding: "utf8" });
    return stdout.trim();
  } catch {
    return path5;
  }
};

// node_modules/define-lazy-prop/index.js
function defineLazyProperty(object, propertyName, valueGetter) {
  const define = (value) => Object.defineProperty(object, propertyName, { value, enumerable: true, writable: true });
  Object.defineProperty(object, propertyName, {
    configurable: true,
    enumerable: true,
    get() {
      const result = valueGetter();
      define(result);
      return result;
    },
    set(value) {
      define(value);
    }
  });
  return object;
}

// node_modules/default-browser/index.js
var import_node_util6 = require("node:util");
var import_node_process5 = __toESM(require("node:process"), 1);
var import_node_child_process6 = require("node:child_process");

// node_modules/default-browser-id/index.js
var import_node_util3 = require("node:util");
var import_node_process3 = __toESM(require("node:process"), 1);
var import_node_child_process3 = require("node:child_process");
var execFileAsync = (0, import_node_util3.promisify)(import_node_child_process3.execFile);
async function defaultBrowserId() {
  if (import_node_process3.default.platform !== "darwin") {
    throw new Error("macOS only");
  }
  const { stdout } = await execFileAsync("defaults", ["read", "com.apple.LaunchServices/com.apple.launchservices.secure", "LSHandlers"]);
  const match = /LSHandlerRoleAll = "(?!-)(?<id>[^"]+?)";\s+?LSHandlerURLScheme = (?:http|https);/.exec(stdout);
  const browserId = match?.groups.id ?? "com.apple.Safari";
  if (browserId === "com.apple.safari") {
    return "com.apple.Safari";
  }
  return browserId;
}

// node_modules/run-applescript/index.js
var import_node_process4 = __toESM(require("node:process"), 1);
var import_node_util4 = require("node:util");
var import_node_child_process4 = require("node:child_process");
var execFileAsync2 = (0, import_node_util4.promisify)(import_node_child_process4.execFile);
async function runAppleScript(script, { humanReadableOutput = true, signal } = {}) {
  if (import_node_process4.default.platform !== "darwin") {
    throw new Error("macOS only");
  }
  const outputArguments = humanReadableOutput ? [] : ["-ss"];
  const execOptions = {};
  if (signal) {
    execOptions.signal = signal;
  }
  const { stdout } = await execFileAsync2("osascript", ["-e", script, outputArguments], execOptions);
  return stdout.trim();
}

// node_modules/bundle-name/index.js
async function bundleName(bundleId) {
  return runAppleScript(`tell application "Finder" to set app_path to application file id "${bundleId}" as string
tell application "System Events" to get value of property list item "CFBundleName" of property list file (app_path & ":Contents:Info.plist")`);
}

// node_modules/default-browser/windows.js
var import_node_util5 = require("node:util");
var import_node_child_process5 = require("node:child_process");
var execFileAsync3 = (0, import_node_util5.promisify)(import_node_child_process5.execFile);
var windowsBrowserProgIds = {
  MSEdgeHTM: { name: "Edge", id: "com.microsoft.edge" },
  // The missing `L` is correct.
  MSEdgeBHTML: { name: "Edge Beta", id: "com.microsoft.edge.beta" },
  MSEdgeDHTML: { name: "Edge Dev", id: "com.microsoft.edge.dev" },
  AppXq0fevzme2pys62n3e0fbqa7peapykr8v: { name: "Edge", id: "com.microsoft.edge.old" },
  ChromeHTML: { name: "Chrome", id: "com.google.chrome" },
  ChromeBHTML: { name: "Chrome Beta", id: "com.google.chrome.beta" },
  ChromeDHTML: { name: "Chrome Dev", id: "com.google.chrome.dev" },
  ChromiumHTM: { name: "Chromium", id: "org.chromium.Chromium" },
  BraveHTML: { name: "Brave", id: "com.brave.Browser" },
  BraveBHTML: { name: "Brave Beta", id: "com.brave.Browser.beta" },
  BraveDHTML: { name: "Brave Dev", id: "com.brave.Browser.dev" },
  BraveSSHTM: { name: "Brave Nightly", id: "com.brave.Browser.nightly" },
  FirefoxURL: { name: "Firefox", id: "org.mozilla.firefox" },
  OperaStable: { name: "Opera", id: "com.operasoftware.Opera" },
  VivaldiHTM: { name: "Vivaldi", id: "com.vivaldi.Vivaldi" },
  "IE.HTTP": { name: "Internet Explorer", id: "com.microsoft.ie" }
};
var _windowsBrowserProgIdMap = new Map(Object.entries(windowsBrowserProgIds));
var UnknownBrowserError = class extends Error {
};
async function defaultBrowser(_execFileAsync = execFileAsync3) {
  const { stdout } = await _execFileAsync("reg", [
    "QUERY",
    " HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice",
    "/v",
    "ProgId"
  ]);
  const match = /ProgId\s*REG_SZ\s*(?<id>\S+)/.exec(stdout);
  if (!match) {
    throw new UnknownBrowserError(`Cannot find Windows browser in stdout: ${JSON.stringify(stdout)}`);
  }
  const { id } = match.groups;
  const dotIndex = id.lastIndexOf(".");
  const hyphenIndex = id.lastIndexOf("-");
  const baseIdByDot = dotIndex === -1 ? void 0 : id.slice(0, dotIndex);
  const baseIdByHyphen = hyphenIndex === -1 ? void 0 : id.slice(0, hyphenIndex);
  return windowsBrowserProgIds[id] ?? windowsBrowserProgIds[baseIdByDot] ?? windowsBrowserProgIds[baseIdByHyphen] ?? { name: id, id };
}

// node_modules/default-browser/index.js
var execFileAsync4 = (0, import_node_util6.promisify)(import_node_child_process6.execFile);
var titleize = (string) => string.toLowerCase().replaceAll(/(?:^|\s|-)\S/g, (x) => x.toUpperCase());
async function defaultBrowser2() {
  if (import_node_process5.default.platform === "darwin") {
    const id = await defaultBrowserId();
    const name = await bundleName(id);
    return { name, id };
  }
  if (import_node_process5.default.platform === "linux") {
    const { stdout } = await execFileAsync4("xdg-mime", ["query", "default", "x-scheme-handler/http"]);
    const id = stdout.trim();
    const name = titleize(id.replace(/.desktop$/, "").replace("-", " "));
    return { name, id };
  }
  if (import_node_process5.default.platform === "win32") {
    return defaultBrowser();
  }
  throw new Error("Only macOS, Linux, and Windows are supported");
}

// node_modules/is-in-ssh/index.js
var import_node_process6 = __toESM(require("node:process"), 1);
var isInSsh = Boolean(import_node_process6.default.env.SSH_CONNECTION || import_node_process6.default.env.SSH_CLIENT || import_node_process6.default.env.SSH_TTY);
var is_in_ssh_default = isInSsh;

// node_modules/open/index.js
var import_meta = {};
var fallbackAttemptSymbol = /* @__PURE__ */ Symbol("fallbackAttempt");
var __dirname = import_meta.url ? import_node_path.default.dirname((0, import_node_url.fileURLToPath)(import_meta.url)) : "";
var localXdgOpenPath = import_node_path.default.join(__dirname, "xdg-open");
var { platform, arch } = import_node_process7.default;
var tryEachApp = async (apps2, opener) => {
  if (apps2.length === 0) {
    return;
  }
  const errors = [];
  for (const app of apps2) {
    try {
      return await opener(app);
    } catch (error) {
      errors.push(error);
    }
  }
  throw new AggregateError(errors, "Failed to open in all supported apps");
};
var baseOpen = async (options) => {
  options = {
    wait: false,
    background: false,
    newInstance: false,
    allowNonzeroExitCode: false,
    ...options
  };
  const isFallbackAttempt = options[fallbackAttemptSymbol] === true;
  delete options[fallbackAttemptSymbol];
  if (Array.isArray(options.app)) {
    return tryEachApp(options.app, (singleApp) => baseOpen({
      ...options,
      app: singleApp,
      [fallbackAttemptSymbol]: true
    }));
  }
  let { name: app, arguments: appArguments = [] } = options.app ?? {};
  appArguments = [...appArguments];
  if (Array.isArray(app)) {
    return tryEachApp(app, (appName) => baseOpen({
      ...options,
      app: {
        name: appName,
        arguments: appArguments
      },
      [fallbackAttemptSymbol]: true
    }));
  }
  if (app === "browser" || app === "browserPrivate") {
    const ids = {
      "com.google.chrome": "chrome",
      "google-chrome.desktop": "chrome",
      "com.brave.browser": "brave",
      "org.mozilla.firefox": "firefox",
      "firefox.desktop": "firefox",
      "com.microsoft.msedge": "edge",
      "com.microsoft.edge": "edge",
      "com.microsoft.edgemac": "edge",
      "microsoft-edge.desktop": "edge",
      "com.apple.safari": "safari"
    };
    const flags = {
      chrome: "--incognito",
      brave: "--incognito",
      firefox: "--private-window",
      edge: "--inPrivate"
      // Safari doesn't support private mode via command line
    };
    let browser;
    if (is_wsl_default) {
      const progId = await wslDefaultBrowser();
      const browserInfo = _windowsBrowserProgIdMap.get(progId);
      browser = browserInfo ?? {};
    } else {
      browser = await defaultBrowser2();
    }
    if (browser.id in ids) {
      const browserName = ids[browser.id.toLowerCase()];
      if (app === "browserPrivate") {
        if (browserName === "safari") {
          throw new Error("Safari doesn't support opening in private mode via command line");
        }
        appArguments.push(flags[browserName]);
      }
      return baseOpen({
        ...options,
        app: {
          name: apps[browserName],
          arguments: appArguments
        }
      });
    }
    throw new Error(`${browser.name} is not supported as a default browser`);
  }
  let command;
  const cliArguments = [];
  const childProcessOptions = {};
  let shouldUseWindowsInWsl = false;
  if (is_wsl_default && !isInsideContainer() && !is_in_ssh_default && !app) {
    shouldUseWindowsInWsl = await canAccessPowerShell();
  }
  if (platform === "darwin") {
    command = "open";
    if (options.wait) {
      cliArguments.push("--wait-apps");
    }
    if (options.background) {
      cliArguments.push("--background");
    }
    if (options.newInstance) {
      cliArguments.push("--new");
    }
    if (app) {
      cliArguments.push("-a", app);
    }
  } else if (platform === "win32" || shouldUseWindowsInWsl) {
    command = await powerShellPath2();
    cliArguments.push(...executePowerShell.argumentsPrefix);
    if (!is_wsl_default) {
      childProcessOptions.windowsVerbatimArguments = true;
    }
    if (is_wsl_default && options.target) {
      options.target = await convertWslPathToWindows(options.target);
    }
    const encodedArguments = ["$ProgressPreference = 'SilentlyContinue';", "Start"];
    if (options.wait) {
      encodedArguments.push("-Wait");
    }
    if (app) {
      encodedArguments.push(executePowerShell.escapeArgument(app));
      if (options.target) {
        appArguments.push(options.target);
      }
    } else if (options.target) {
      encodedArguments.push(executePowerShell.escapeArgument(options.target));
    }
    if (appArguments.length > 0) {
      appArguments = appArguments.map((argument) => executePowerShell.escapeArgument(argument));
      encodedArguments.push("-ArgumentList", appArguments.join(","));
    }
    options.target = executePowerShell.encodeCommand(encodedArguments.join(" "));
    if (!options.wait) {
      childProcessOptions.stdio = "ignore";
    }
  } else {
    if (app) {
      command = app;
    } else {
      const isBundled = !__dirname || __dirname === "/";
      let exeLocalXdgOpen = false;
      try {
        await import_promises2.default.access(localXdgOpenPath, import_promises2.constants.X_OK);
        exeLocalXdgOpen = true;
      } catch {
      }
      const useSystemXdgOpen = import_node_process7.default.versions.electron ?? (platform === "android" || isBundled || !exeLocalXdgOpen);
      command = useSystemXdgOpen ? "xdg-open" : localXdgOpenPath;
    }
    if (appArguments.length > 0) {
      cliArguments.push(...appArguments);
    }
    if (!options.wait) {
      childProcessOptions.stdio = "ignore";
      childProcessOptions.detached = true;
    }
  }
  if (platform === "darwin" && appArguments.length > 0) {
    cliArguments.push("--args", ...appArguments);
  }
  if (options.target) {
    cliArguments.push(options.target);
  }
  const subprocess = import_node_child_process7.default.spawn(command, cliArguments, childProcessOptions);
  if (options.wait) {
    return new Promise((resolve, reject) => {
      subprocess.once("error", reject);
      subprocess.once("close", (exitCode) => {
        if (!options.allowNonzeroExitCode && exitCode !== 0) {
          reject(new Error(`Exited with code ${exitCode}`));
          return;
        }
        resolve(subprocess);
      });
    });
  }
  if (isFallbackAttempt) {
    return new Promise((resolve, reject) => {
      subprocess.once("error", reject);
      subprocess.once("spawn", () => {
        subprocess.once("close", (exitCode) => {
          subprocess.off("error", reject);
          if (exitCode !== 0) {
            reject(new Error(`Exited with code ${exitCode}`));
            return;
          }
          subprocess.unref();
          resolve(subprocess);
        });
      });
    });
  }
  subprocess.unref();
  return new Promise((resolve, reject) => {
    subprocess.once("error", reject);
    subprocess.once("spawn", () => {
      subprocess.off("error", reject);
      resolve(subprocess);
    });
  });
};
var open = (target, options) => {
  if (typeof target !== "string") {
    throw new TypeError("Expected a `target`");
  }
  return baseOpen({
    ...options,
    target
  });
};
function detectArchBinary(binary) {
  if (typeof binary === "string" || Array.isArray(binary)) {
    return binary;
  }
  const { [arch]: archBinary } = binary;
  if (!archBinary) {
    throw new Error(`${arch} is not supported`);
  }
  return archBinary;
}
function detectPlatformBinary({ [platform]: platformBinary }, { wsl } = {}) {
  if (wsl && is_wsl_default) {
    return detectArchBinary(wsl);
  }
  if (!platformBinary) {
    throw new Error(`${platform} is not supported`);
  }
  return detectArchBinary(platformBinary);
}
var apps = {
  browser: "browser",
  browserPrivate: "browserPrivate"
};
defineLazyProperty(apps, "chrome", () => detectPlatformBinary({
  darwin: "google chrome",
  win32: "chrome",
  // `chromium-browser` is the older deb package name used by Ubuntu/Debian before snap.
  linux: ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]
}, {
  wsl: {
    ia32: "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    x64: ["/mnt/c/Program Files/Google/Chrome/Application/chrome.exe", "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"]
  }
}));
defineLazyProperty(apps, "brave", () => detectPlatformBinary({
  darwin: "brave browser",
  win32: "brave",
  linux: ["brave-browser", "brave"]
}, {
  wsl: {
    ia32: "/mnt/c/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe",
    x64: ["/mnt/c/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe", "/mnt/c/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"]
  }
}));
defineLazyProperty(apps, "firefox", () => detectPlatformBinary({
  darwin: "firefox",
  win32: String.raw`C:\Program Files\Mozilla Firefox\firefox.exe`,
  linux: "firefox"
}, {
  wsl: "/mnt/c/Program Files/Mozilla Firefox/firefox.exe"
}));
defineLazyProperty(apps, "edge", () => detectPlatformBinary({
  darwin: "microsoft edge",
  win32: "msedge",
  linux: ["microsoft-edge", "microsoft-edge-dev"]
}, {
  wsl: "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
}));
defineLazyProperty(apps, "safari", () => detectPlatformBinary({
  darwin: "Safari"
}));
var open_default = open;

// src/utils/notifications.mjs
var WEBCHAT = "webchat";
function parseNotify(notify) {
  if (!notify) {
    return { channel: null, target: null };
  }
  if (!notify.includes(":")) {
    return { channel: notify, target: null };
  }
  const [channel, ...targetParts] = notify.split(":");
  const target = targetParts.join(":");
  return { channel, target };
}

// src/utils/redact.mjs
function shannonEntropy(str) {
  if (!str) {
    return 0;
  }
  const len = str.length;
  const frequencies = {};
  for (let i = 0; i < len; i++) {
    const char = str[i];
    frequencies[char] = (frequencies[char] || 0) + 1;
  }
  let entropy = 0;
  for (const char in frequencies) {
    const frequency = frequencies[char] / len;
    entropy -= frequency * Math.log2(frequency);
  }
  return entropy;
}
var SECRET_PATTERNS = [
  // Bearer
  [/(bearer\s+)([a-zA-Z0-9\-._~+/]+=*)/gi, "$1[REDACTED]"],
  // URI with credentials
  [/(:\/\/)([^:]+):([^@]+@)/gi, "$1$2:[REDACTED]@"],
  // Command-line flags with space-separated secrets, e.g. --password my-secret
  [/((?:--|-)(?:api[-_]?key|access[-_]?token|auth[-_]?token|secret|token|password|passwd|pwd)|-p)\s+([^-\s][\S]*)/gi, "$1 [REDACTED]"],
  // Command-line flags with equals-separated secrets, e.g. --password=my-secret
  [/((?:--|-)(?:api[-_]?key|access[-_]?token|auth[-_]?token|secret|token|password|passwd|pwd))=([^\s]+)/gi, "$1=[REDACTED]"],
  // Generic assignments
  [/((?:api[-_]?key|secret|token|password|passwd|pwd)\s*[:=]\s*['"]?)([^'"\s]+)/gi, "$1[REDACTED]"],
  // Environment variable assignments
  [/\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASSWD|PWD|API_KEY|ACCESS_KEY)[A-Z0-9_]*)=([^\s]+)/g, "$1=[REDACTED]"],
  // curl headers
  [/(-H\s+["']?(?:Authorization|X-API-Key):\s*)([^"']+)/gi, "$1[REDACTED]"],
  // Generic JWTs
  [/\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9._-]+\.[A-Za-z0-9._-]+\b/g, "[REDACTED]"],
  // OpenAI API keys
  [/\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b/g, "[REDACTED]"],
  // Anthropic API keys
  [/\bsk-ant-[A-Za-z0-9\-_]{20,}\b/g, "[REDACTED]"],
  // Google / Gemini API keys
  [/\bAIza[0-9A-Za-z\-_]{35}\b/g, "[REDACTED]"],
  // AWS access keys
  [/\bA(?:AG|CC|GP|ID|IP|KI|NP|NV|PK|RO|SC|SI)A[A-Z0-9]{16}\b/g, "[REDACTED]"],
  // AWS session tokens
  [/\bFwoGZXIvYXdzE[A-Za-z0-9\/+=]{20,}\b/g, "[REDACTED]"],
  // GitHub tokens
  [/\bgh[pous]_[A-Za-z0-9]{36}\b/g, "[REDACTED]"],
  // Slack webhooks
  [/https:\/\/hooks\.slack\.com\/services\/[A-Z0-9]{9}\/[A-Z0-9]{9}\/[A-Za-z0-9]+/gi, "[REDACTED]"],
  // PEM private keys
  [/-----BEGIN[\s\S]+?PRIVATE KEY-----[\s\S]+?-----END[\s\S]+?PRIVATE KEY-----/g, "[REDACTED]"]
];
function redact(text) {
  if (typeof text !== "string") {
    return text;
  }
  let redactedText = text;
  for (const [pattern, replacement] of SECRET_PATTERNS) {
    redactedText = redactedText.replace(pattern, replacement);
  }
  const MIN_ENTROPY = 4.3;
  const MIN_LENGTH = 20;
  const HIGH_ENTROPY_PATTERN = new RegExp(`[A-Za-z0-9\\-_+/=]{${MIN_LENGTH},}`, "g");
  redactedText = redactedText.replace(HIGH_ENTROPY_PATTERN, (match) => {
    if (shannonEntropy(match) > MIN_ENTROPY) {
      return "[REDACTED]";
    }
    return match;
  });
  return redactedText;
}

// src/services/IdentityGateWay.mjs
var APPROVAL_STATUS = {
  APPROVED: "approved",
  DENIED: "deny",
  API_KEY_CREATED: "api_key_created"
};
var IdentityGateWay = class {
  #loginIdService;
  #notificationService;
  #envManager;
  #commandExecutor;
  #config;
  constructor({ loginIdService, notificationService: notificationService2, envManager: envManager2, commandExecutor: commandExecutor2, config: config2 }) {
    this.#loginIdService = loginIdService;
    this.#notificationService = notificationService2;
    this.#envManager = envManager2;
    this.#commandExecutor = commandExecutor2;
    this.#config = config2;
  }
  #notify(notify, message) {
    if (notify && this.#notificationService) {
      const { channel, target } = parseNotify(notify);
      if (channel && target) {
        this.#notificationService.notify(message, channel, target);
      }
    }
  }
  async createAuthSession() {
    const { topic, link: authUrl } = await this.#loginIdService.createAuthSession();
    if (!topic) {
      throw new Error("Authentication session is not found");
    }
    return { authUrl, topic };
  }
  async approvalInit(toolCall, displayString) {
    const redactedToolCall = redact(toolCall);
    const redactedDisplayString = redact(displayString);
    const result = await this.#loginIdService.approvalInit(redactedToolCall, redactedDisplayString);
    const { approvalUrl, topic } = result;
    return { approvalUrl, topic };
  }
  async #handleSessionWait(topic, url, { notify, notificationMessage }) {
    if (url) {
      let notificationSent = false;
      if (notify && this.#notificationService) {
        const { channel, target } = parseNotify(notify);
        if (channel === WEBCHAT) {
          open_default(url.toString());
          notificationSent = true;
        } else if (channel && target) {
          const message = notificationMessage.replace("{{url}}", url.toString());
          notificationSent = this.#notificationService.notify(
            message,
            channel,
            target
          );
        }
      }
      if (!notificationSent) {
        console.log(`Falling back to opening browser.`);
        open_default(url.toString());
      }
    }
    return await this.#loginIdService.waitForSession(topic);
  }
  async approvalWait(topic, approvalUrl, { notify } = {}) {
    const notificationMessage = "An action requires your approval. Please visit this URL to review: {{url}}";
    const eventData = await this.#handleSessionWait(topic, approvalUrl, { notify, notificationMessage });
    if (eventData?.status?.toLowerCase() === APPROVAL_STATUS.APPROVED) {
      return JSON.stringify({ status: "approved" });
    } else {
      this.#notify(notify, "The action was denied.");
      return JSON.stringify({ status: "deny" });
    }
  }
  async authFlow({ notify } = {}) {
    if (this.#config.hasCredentials) {
      throw new Error("Onboarding has already been completed. You cannot create another onboarding session.");
    }
    const { authUrl, topic } = await this.createAuthSession();
    const notificationMessage = "Please visit this URL to complete onboarding: {{url}}";
    const eventData = await this.#handleSessionWait(topic, authUrl, { notify, notificationMessage });
    if (eventData?.status?.toLowerCase() === APPROVAL_STATUS.API_KEY_CREATED) {
      const { meta } = eventData;
      const { api_key, key_id } = meta;
      await this.#envManager.saveCredentials(key_id, api_key);
      await this.#envManager.updateAgentMarkdown();
      this.#notify(notify, "Onboarding successful. Credentials have been saved.");
      return { success: true, message: "Credentials are captured" };
    } else {
      this.#notify(notify, "Onboarding failed. Could not create credentials.");
      return { success: false, message: "Could not create credentials" };
    }
  }
  async approvalFlow(toolCall, displayString, { notify } = {}) {
    const { approvalUrl, topic } = await this.approvalInit(toolCall, displayString);
    try {
      const resultStr = await this.approvalWait(topic, approvalUrl, { notify });
      const result = JSON.parse(resultStr);
      if (result.status === APPROVAL_STATUS.APPROVED) {
        if (this.#commandExecutor) {
          const { error, stdout, stderr } = await this.#commandExecutor.execute(toolCall);
          if (error) {
            this.#notify(notify, `Execution failed for command: \`${toolCall}\`. Error: ${stderr || error.message}`);
            return {
              status: "approved_but_execution_failed",
              error: stderr || error.message,
              stdout
            };
          } else {
            this.#notify(notify, `Successfully executed command: \`${toolCall}\``);
            return {
              status: "approved_and_executed",
              stdout,
              stderr
            };
          }
        }
        return {
          status: "approved"
        };
      } else {
        return {
          status: "deny"
        };
      }
    } catch (error) {
      return {
        status: "deny"
      };
    }
  }
  async cleanupFlow({ notify } = {}) {
    const actionDescription = "Uninstall AgentAuth skill";
    const { approvalUrl, topic } = await this.approvalInit(
      actionDescription,
      actionDescription
    );
    const resultStr = await this.approvalWait(topic, approvalUrl, { notify });
    const result = JSON.parse(resultStr);
    if (result.status === APPROVAL_STATUS.APPROVED) {
      await this.#envManager.restoreAgentMarkdown();
      console.log("AgentAuth cleanup completed");
    } else {
      console.log("AgentAuth cleanup was denied.");
    }
  }
};

// src/cli/commands/BaseCommand.mjs
var BaseCommand = class {
  async execute(args) {
    throw new Error("execute() must be implemented by subclasses");
  }
};

// src/cli/commands/ApprovalFlowCommand.mjs
var ApprovalFlowCommand = class extends BaseCommand {
  constructor(idgwService2) {
    super();
    this.idgwService = idgwService2;
  }
  async execute(args) {
    const { toolCall, displayString, notify } = args;
    return this.idgwService.approvalFlow(toolCall, displayString, { notify });
  }
};

// src/cli/commands/AuthFlowCommand.mjs
var AuthFlowCommand = class extends BaseCommand {
  constructor(idgwService2) {
    super();
    this.idgwService = idgwService2;
  }
  async execute(args) {
    const { notify } = args;
    return this.idgwService.authFlow({ notify });
  }
};

// src/cli/commands/TestNotifyCommand.mjs
var TestNotifyCommand = class extends BaseCommand {
  constructor(notificationService2) {
    super();
    this.notificationService = notificationService2;
  }
  async execute(args) {
    const { message, notify } = args;
    const { channel, target } = parseNotify(notify);
    const success = this.notificationService.notify(message, channel, target);
    if (success) {
      console.log("Notification sent successfully.");
    }
  }
};

// src/cli/commands/CleanupCommand.mjs
var CleanupCommand = class extends BaseCommand {
  constructor(idgwService2) {
    super();
    this.idgwService = idgwService2;
  }
  async execute(args) {
    const { notify } = args;
    return this.idgwService.cleanupFlow({ notify });
  }
};

// src/services/HttpClient.mjs
var HttpClient = class {
  constructor({ signer } = {}) {
    this.signer = signer;
  }
  async post(url, body, options = {}) {
    return await this.#request(url, {
      method: "POST",
      body: JSON.stringify(body),
      ...options
    });
  }
  async #request(url, options = {}) {
    let {
      method = "GET",
      headers = {},
      body,
      ...rest
    } = options;
    let finalHeaders = {
      "content-type": "application/json",
      ...headers
    };
    const request = new Request(url, {
      method,
      headers: finalHeaders,
      body,
      ...rest
    });
    if (this.signer) {
      const signed = await this.signer.sign(request);
      if (signed instanceof Request) {
        finalHeaders = Object.fromEntries(signed.headers.entries());
      } else {
        finalHeaders = {
          ...finalHeaders,
          ...signed
        };
      }
    }
    const res = await fetch(url, {
      method,
      headers: finalHeaders,
      body,
      ...rest
    });
    if (res.status === 204) {
      return void 0;
    }
    const prefixApiErrorMessage = (message) => `API Error: ${message}`;
    let responseBody;
    try {
      responseBody = await res.json();
    } catch (e) {
      if (!res.ok) {
        throw new Error(
          prefixApiErrorMessage(`${res.status} ${res.statusText}`)
        );
      }
      return void 0;
    }
    if (responseBody?.errors) {
      const firstError = responseBody.errors?.[0] || {};
      const message = firstError.message || JSON.stringify(responseBody.errors);
      throw new Error(prefixApiErrorMessage(message));
    }
    if (!res.ok) {
      const message = responseBody?.message || res.status;
      throw new Error(prefixApiErrorMessage(message));
    }
    return responseBody;
  }
};

// src/utils/AgentSigner.mjs
var import_crypto = require("crypto");
var import_http_message_signatures = __toESM(require_lib(), 1);
var AgentSigner = class {
  #key;
  constructor(privateKey, keyId) {
    if (!privateKey) {
      throw new Error("Private key is required for AgentSigner");
    }
    if (!keyId) {
      throw new Error("Key ID is required for AgentSigner");
    }
    const pKey = (0, import_crypto.createPrivateKey)(privateKey);
    this.#key = (0, import_http_message_signatures.createSigner)(pKey, "rsa-pss-sha512", keyId);
  }
  async sign(request) {
    const requestOptions = {
      method: request.method,
      url: request.url,
      headers: Object.fromEntries(request.headers.entries())
    };
    const fieldsToSign = ["@method", "@target-uri", "content-type"];
    const body = await request.clone().text();
    if (body) {
      requestOptions.body = body;
      const digest = (0, import_crypto.createHash)("sha512").update(body).digest("base64");
      requestOptions.headers["content-digest"] = `sha-512=:${digest}:`;
      fieldsToSign.push("content-digest");
    }
    const signedRequest = await import_http_message_signatures.httpbis.signMessage(
      {
        key: this.#key,
        fields: fieldsToSign,
        name: "sig1",
        paramValues: {
          created: /* @__PURE__ */ new Date(),
          expires: new Date(Date.now() + 15e4)
        }
      },
      requestOptions
    );
    return signedRequest.headers;
  }
};

// node_modules/eventsource-parser/dist/index.js
var ParseError = class extends Error {
  constructor(message, options) {
    super(message), this.name = "ParseError", this.type = options.type, this.field = options.field, this.value = options.value, this.line = options.line;
  }
};
function noop(_arg) {
}
function createParser(callbacks) {
  if (typeof callbacks == "function")
    throw new TypeError(
      "`callbacks` must be an object, got a function instead. Did you mean `{onEvent: fn}`?"
    );
  const { onEvent = noop, onError = noop, onRetry = noop, onComment } = callbacks;
  let incompleteLine = "", isFirstChunk = true, id, data = "", eventType = "";
  function feed(newChunk) {
    const chunk = isFirstChunk ? newChunk.replace(/^\xEF\xBB\xBF/, "") : newChunk, [complete, incomplete] = splitLines(`${incompleteLine}${chunk}`);
    for (const line of complete)
      parseLine(line);
    incompleteLine = incomplete, isFirstChunk = false;
  }
  function parseLine(line) {
    if (line === "") {
      dispatchEvent();
      return;
    }
    if (line.startsWith(":")) {
      onComment && onComment(line.slice(line.startsWith(": ") ? 2 : 1));
      return;
    }
    const fieldSeparatorIndex = line.indexOf(":");
    if (fieldSeparatorIndex !== -1) {
      const field = line.slice(0, fieldSeparatorIndex), offset = line[fieldSeparatorIndex + 1] === " " ? 2 : 1, value = line.slice(fieldSeparatorIndex + offset);
      processField(field, value, line);
      return;
    }
    processField(line, "", line);
  }
  function processField(field, value, line) {
    switch (field) {
      case "event":
        eventType = value;
        break;
      case "data":
        data = `${data}${value}
`;
        break;
      case "id":
        id = value.includes("\0") ? void 0 : value;
        break;
      case "retry":
        /^\d+$/.test(value) ? onRetry(parseInt(value, 10)) : onError(
          new ParseError(`Invalid \`retry\` value: "${value}"`, {
            type: "invalid-retry",
            value,
            line
          })
        );
        break;
      default:
        onError(
          new ParseError(
            `Unknown field "${field.length > 20 ? `${field.slice(0, 20)}\u2026` : field}"`,
            { type: "unknown-field", field, value, line }
          )
        );
        break;
    }
  }
  function dispatchEvent() {
    data.length > 0 && onEvent({
      id,
      event: eventType || void 0,
      // If the data buffer's last character is a U+000A LINE FEED (LF) character,
      // then remove the last character from the data buffer.
      data: data.endsWith(`
`) ? data.slice(0, -1) : data
    }), id = void 0, data = "", eventType = "";
  }
  function reset(options = {}) {
    incompleteLine && options.consume && parseLine(incompleteLine), isFirstChunk = true, id = void 0, data = "", eventType = "", incompleteLine = "";
  }
  return { feed, reset };
}
function splitLines(chunk) {
  const lines = [];
  let incompleteLine = "", searchIndex = 0;
  for (; searchIndex < chunk.length; ) {
    const crIndex = chunk.indexOf("\r", searchIndex), lfIndex = chunk.indexOf(`
`, searchIndex);
    let lineEnd = -1;
    if (crIndex !== -1 && lfIndex !== -1 ? lineEnd = Math.min(crIndex, lfIndex) : crIndex !== -1 ? crIndex === chunk.length - 1 ? lineEnd = -1 : lineEnd = crIndex : lfIndex !== -1 && (lineEnd = lfIndex), lineEnd === -1) {
      incompleteLine = chunk.slice(searchIndex);
      break;
    } else {
      const line = chunk.slice(searchIndex, lineEnd);
      lines.push(line), searchIndex = lineEnd + 1, chunk[searchIndex - 1] === "\r" && chunk[searchIndex] === `
` && searchIndex++;
    }
  }
  return [lines, incompleteLine];
}

// node_modules/eventsource/dist/index.js
var ErrorEvent = class extends Event {
  /**
   * Constructs a new `ErrorEvent` instance. This is typically not called directly,
   * but rather emitted by the `EventSource` object when an error occurs.
   *
   * @param type - The type of the event (should be "error")
   * @param errorEventInitDict - Optional properties to include in the error event
   */
  constructor(type, errorEventInitDict) {
    var _a, _b;
    super(type), this.code = (_a = errorEventInitDict == null ? void 0 : errorEventInitDict.code) != null ? _a : void 0, this.message = (_b = errorEventInitDict == null ? void 0 : errorEventInitDict.message) != null ? _b : void 0;
  }
  /**
   * Node.js "hides" the `message` and `code` properties of the `ErrorEvent` instance,
   * when it is `console.log`'ed. This makes it harder to debug errors. To ease debugging,
   * we explicitly include the properties in the `inspect` method.
   *
   * This is automatically called by Node.js when you `console.log` an instance of this class.
   *
   * @param _depth - The current depth
   * @param options - The options passed to `util.inspect`
   * @param inspect - The inspect function to use (prevents having to import it from `util`)
   * @returns A string representation of the error
   */
  [/* @__PURE__ */ Symbol.for("nodejs.util.inspect.custom")](_depth, options, inspect) {
    return inspect(inspectableError(this), options);
  }
  /**
   * Deno "hides" the `message` and `code` properties of the `ErrorEvent` instance,
   * when it is `console.log`'ed. This makes it harder to debug errors. To ease debugging,
   * we explicitly include the properties in the `inspect` method.
   *
   * This is automatically called by Deno when you `console.log` an instance of this class.
   *
   * @param inspect - The inspect function to use (prevents having to import it from `util`)
   * @param options - The options passed to `Deno.inspect`
   * @returns A string representation of the error
   */
  [/* @__PURE__ */ Symbol.for("Deno.customInspect")](inspect, options) {
    return inspect(inspectableError(this), options);
  }
};
function syntaxError(message) {
  const DomException = globalThis.DOMException;
  return typeof DomException == "function" ? new DomException(message, "SyntaxError") : new SyntaxError(message);
}
function flattenError(err) {
  return err instanceof Error ? "errors" in err && Array.isArray(err.errors) ? err.errors.map(flattenError).join(", ") : "cause" in err && err.cause instanceof Error ? `${err}: ${flattenError(err.cause)}` : err.message : `${err}`;
}
function inspectableError(err) {
  return {
    type: err.type,
    message: err.message,
    code: err.code,
    defaultPrevented: err.defaultPrevented,
    cancelable: err.cancelable,
    timeStamp: err.timeStamp
  };
}
var __typeError = (msg) => {
  throw TypeError(msg);
};
var __accessCheck = (obj, member, msg) => member.has(obj) || __typeError("Cannot " + msg);
var __privateGet = (obj, member, getter) => (__accessCheck(obj, member, "read from private field"), getter ? getter.call(obj) : member.get(obj));
var __privateAdd = (obj, member, value) => member.has(obj) ? __typeError("Cannot add the same private member more than once") : member instanceof WeakSet ? member.add(obj) : member.set(obj, value);
var __privateSet = (obj, member, value, setter) => (__accessCheck(obj, member, "write to private field"), member.set(obj, value), value);
var __privateMethod = (obj, member, method) => (__accessCheck(obj, member, "access private method"), method);
var _readyState;
var _url;
var _redirectUrl;
var _withCredentials;
var _fetch;
var _reconnectInterval;
var _reconnectTimer;
var _lastEventId;
var _controller;
var _parser;
var _onError;
var _onMessage;
var _onOpen;
var _EventSource_instances;
var connect_fn;
var _onFetchResponse;
var _onFetchError;
var getRequestOptions_fn;
var _onEvent;
var _onRetryChange;
var failConnection_fn;
var scheduleReconnect_fn;
var _reconnect;
var EventSource = class extends EventTarget {
  constructor(url, eventSourceInitDict) {
    var _a, _b;
    super(), __privateAdd(this, _EventSource_instances), this.CONNECTING = 0, this.OPEN = 1, this.CLOSED = 2, __privateAdd(this, _readyState), __privateAdd(this, _url), __privateAdd(this, _redirectUrl), __privateAdd(this, _withCredentials), __privateAdd(this, _fetch), __privateAdd(this, _reconnectInterval), __privateAdd(this, _reconnectTimer), __privateAdd(this, _lastEventId, null), __privateAdd(this, _controller), __privateAdd(this, _parser), __privateAdd(this, _onError, null), __privateAdd(this, _onMessage, null), __privateAdd(this, _onOpen, null), __privateAdd(this, _onFetchResponse, async (response) => {
      var _a2;
      __privateGet(this, _parser).reset();
      const { body, redirected, status, headers } = response;
      if (status === 204) {
        __privateMethod(this, _EventSource_instances, failConnection_fn).call(this, "Server sent HTTP 204, not reconnecting", 204), this.close();
        return;
      }
      if (redirected ? __privateSet(this, _redirectUrl, new URL(response.url)) : __privateSet(this, _redirectUrl, void 0), status !== 200) {
        __privateMethod(this, _EventSource_instances, failConnection_fn).call(this, `Non-200 status code (${status})`, status);
        return;
      }
      if (!(headers.get("content-type") || "").startsWith("text/event-stream")) {
        __privateMethod(this, _EventSource_instances, failConnection_fn).call(this, 'Invalid content type, expected "text/event-stream"', status);
        return;
      }
      if (__privateGet(this, _readyState) === this.CLOSED)
        return;
      __privateSet(this, _readyState, this.OPEN);
      const openEvent = new Event("open");
      if ((_a2 = __privateGet(this, _onOpen)) == null || _a2.call(this, openEvent), this.dispatchEvent(openEvent), typeof body != "object" || !body || !("getReader" in body)) {
        __privateMethod(this, _EventSource_instances, failConnection_fn).call(this, "Invalid response body, expected a web ReadableStream", status), this.close();
        return;
      }
      const decoder = new TextDecoder(), reader = body.getReader();
      let open2 = true;
      do {
        const { done, value } = await reader.read();
        value && __privateGet(this, _parser).feed(decoder.decode(value, { stream: !done })), done && (open2 = false, __privateGet(this, _parser).reset(), __privateMethod(this, _EventSource_instances, scheduleReconnect_fn).call(this));
      } while (open2);
    }), __privateAdd(this, _onFetchError, (err) => {
      __privateSet(this, _controller, void 0), !(err.name === "AbortError" || err.type === "aborted") && __privateMethod(this, _EventSource_instances, scheduleReconnect_fn).call(this, flattenError(err));
    }), __privateAdd(this, _onEvent, (event) => {
      typeof event.id == "string" && __privateSet(this, _lastEventId, event.id);
      const messageEvent = new MessageEvent(event.event || "message", {
        data: event.data,
        origin: __privateGet(this, _redirectUrl) ? __privateGet(this, _redirectUrl).origin : __privateGet(this, _url).origin,
        lastEventId: event.id || ""
      });
      __privateGet(this, _onMessage) && (!event.event || event.event === "message") && __privateGet(this, _onMessage).call(this, messageEvent), this.dispatchEvent(messageEvent);
    }), __privateAdd(this, _onRetryChange, (value) => {
      __privateSet(this, _reconnectInterval, value);
    }), __privateAdd(this, _reconnect, () => {
      __privateSet(this, _reconnectTimer, void 0), __privateGet(this, _readyState) === this.CONNECTING && __privateMethod(this, _EventSource_instances, connect_fn).call(this);
    });
    try {
      if (url instanceof URL)
        __privateSet(this, _url, url);
      else if (typeof url == "string")
        __privateSet(this, _url, new URL(url, getBaseURL()));
      else
        throw new Error("Invalid URL");
    } catch {
      throw syntaxError("An invalid or illegal string was specified");
    }
    __privateSet(this, _parser, createParser({
      onEvent: __privateGet(this, _onEvent),
      onRetry: __privateGet(this, _onRetryChange)
    })), __privateSet(this, _readyState, this.CONNECTING), __privateSet(this, _reconnectInterval, 3e3), __privateSet(this, _fetch, (_a = eventSourceInitDict == null ? void 0 : eventSourceInitDict.fetch) != null ? _a : globalThis.fetch), __privateSet(this, _withCredentials, (_b = eventSourceInitDict == null ? void 0 : eventSourceInitDict.withCredentials) != null ? _b : false), __privateMethod(this, _EventSource_instances, connect_fn).call(this);
  }
  /**
   * Returns the state of this EventSource object's connection. It can have the values described below.
   *
   * [MDN Reference](https://developer.mozilla.org/docs/Web/API/EventSource/readyState)
   *
   * Note: typed as `number` instead of `0 | 1 | 2` for compatibility with the `EventSource` interface,
   * defined in the TypeScript `dom` library.
   *
   * @public
   */
  get readyState() {
    return __privateGet(this, _readyState);
  }
  /**
   * Returns the URL providing the event stream.
   *
   * [MDN Reference](https://developer.mozilla.org/docs/Web/API/EventSource/url)
   *
   * @public
   */
  get url() {
    return __privateGet(this, _url).href;
  }
  /**
   * Returns true if the credentials mode for connection requests to the URL providing the event stream is set to "include", and false otherwise.
   *
   * [MDN Reference](https://developer.mozilla.org/docs/Web/API/EventSource/withCredentials)
   */
  get withCredentials() {
    return __privateGet(this, _withCredentials);
  }
  /** [MDN Reference](https://developer.mozilla.org/docs/Web/API/EventSource/error_event) */
  get onerror() {
    return __privateGet(this, _onError);
  }
  set onerror(value) {
    __privateSet(this, _onError, value);
  }
  /** [MDN Reference](https://developer.mozilla.org/docs/Web/API/EventSource/message_event) */
  get onmessage() {
    return __privateGet(this, _onMessage);
  }
  set onmessage(value) {
    __privateSet(this, _onMessage, value);
  }
  /** [MDN Reference](https://developer.mozilla.org/docs/Web/API/EventSource/open_event) */
  get onopen() {
    return __privateGet(this, _onOpen);
  }
  set onopen(value) {
    __privateSet(this, _onOpen, value);
  }
  addEventListener(type, listener, options) {
    const listen = listener;
    super.addEventListener(type, listen, options);
  }
  removeEventListener(type, listener, options) {
    const listen = listener;
    super.removeEventListener(type, listen, options);
  }
  /**
   * Aborts any instances of the fetch algorithm started for this EventSource object, and sets the readyState attribute to CLOSED.
   *
   * [MDN Reference](https://developer.mozilla.org/docs/Web/API/EventSource/close)
   *
   * @public
   */
  close() {
    __privateGet(this, _reconnectTimer) && clearTimeout(__privateGet(this, _reconnectTimer)), __privateGet(this, _readyState) !== this.CLOSED && (__privateGet(this, _controller) && __privateGet(this, _controller).abort(), __privateSet(this, _readyState, this.CLOSED), __privateSet(this, _controller, void 0));
  }
};
_readyState = /* @__PURE__ */ new WeakMap(), _url = /* @__PURE__ */ new WeakMap(), _redirectUrl = /* @__PURE__ */ new WeakMap(), _withCredentials = /* @__PURE__ */ new WeakMap(), _fetch = /* @__PURE__ */ new WeakMap(), _reconnectInterval = /* @__PURE__ */ new WeakMap(), _reconnectTimer = /* @__PURE__ */ new WeakMap(), _lastEventId = /* @__PURE__ */ new WeakMap(), _controller = /* @__PURE__ */ new WeakMap(), _parser = /* @__PURE__ */ new WeakMap(), _onError = /* @__PURE__ */ new WeakMap(), _onMessage = /* @__PURE__ */ new WeakMap(), _onOpen = /* @__PURE__ */ new WeakMap(), _EventSource_instances = /* @__PURE__ */ new WeakSet(), /**
* Connect to the given URL and start receiving events
*
* @internal
*/
connect_fn = function() {
  __privateSet(this, _readyState, this.CONNECTING), __privateSet(this, _controller, new AbortController()), __privateGet(this, _fetch)(__privateGet(this, _url), __privateMethod(this, _EventSource_instances, getRequestOptions_fn).call(this)).then(__privateGet(this, _onFetchResponse)).catch(__privateGet(this, _onFetchError));
}, _onFetchResponse = /* @__PURE__ */ new WeakMap(), _onFetchError = /* @__PURE__ */ new WeakMap(), /**
* Get request options for the `fetch()` request
*
* @returns The request options
* @internal
*/
getRequestOptions_fn = function() {
  var _a;
  const init = {
    // [spec] Let `corsAttributeState` be `Anonymous`…
    // [spec] …will have their mode set to "cors"…
    mode: "cors",
    redirect: "follow",
    headers: { Accept: "text/event-stream", ...__privateGet(this, _lastEventId) ? { "Last-Event-ID": __privateGet(this, _lastEventId) } : void 0 },
    cache: "no-store",
    signal: (_a = __privateGet(this, _controller)) == null ? void 0 : _a.signal
  };
  return "window" in globalThis && (init.credentials = this.withCredentials ? "include" : "same-origin"), init;
}, _onEvent = /* @__PURE__ */ new WeakMap(), _onRetryChange = /* @__PURE__ */ new WeakMap(), /**
* Handles the process referred to in the EventSource specification as "failing a connection".
*
* @param error - The error causing the connection to fail
* @param code - The HTTP status code, if available
* @internal
*/
failConnection_fn = function(message, code) {
  var _a;
  __privateGet(this, _readyState) !== this.CLOSED && __privateSet(this, _readyState, this.CLOSED);
  const errorEvent = new ErrorEvent("error", { code, message });
  (_a = __privateGet(this, _onError)) == null || _a.call(this, errorEvent), this.dispatchEvent(errorEvent);
}, /**
* Schedules a reconnection attempt against the EventSource endpoint.
*
* @param message - The error causing the connection to fail
* @param code - The HTTP status code, if available
* @internal
*/
scheduleReconnect_fn = function(message, code) {
  var _a;
  if (__privateGet(this, _readyState) === this.CLOSED)
    return;
  __privateSet(this, _readyState, this.CONNECTING);
  const errorEvent = new ErrorEvent("error", { code, message });
  (_a = __privateGet(this, _onError)) == null || _a.call(this, errorEvent), this.dispatchEvent(errorEvent), __privateSet(this, _reconnectTimer, setTimeout(__privateGet(this, _reconnect), __privateGet(this, _reconnectInterval)));
}, _reconnect = /* @__PURE__ */ new WeakMap(), /**
* ReadyState representing an EventSource currently trying to connect
*
* @public
*/
EventSource.CONNECTING = 0, /**
* ReadyState representing an EventSource connection that is open (eg connected)
*
* @public
*/
EventSource.OPEN = 1, /**
* ReadyState representing an EventSource connection that is closed (eg disconnected)
*
* @public
*/
EventSource.CLOSED = 2;
Object.defineProperty(EventSource, /* @__PURE__ */ Symbol.for("eventsource.supports-fetch-override"), {
  value: true,
  writable: false,
  configurable: false,
  enumerable: false
});
function getBaseURL() {
  const doc = "document" in globalThis ? globalThis.document : void 0;
  return doc && typeof doc == "object" && "baseURI" in doc && typeof doc.baseURI == "string" ? doc.baseURI : void 0;
}

// src/services/SseClient.mjs
var SseClient = class {
  constructor({ signer } = {}) {
    this.signer = signer;
  }
  async waitForEvent(url, { eventName, timeout = 6e4 }) {
    return new Promise(async (resolve, reject) => {
      let eventSource;
      const timeoutId = setTimeout(() => {
        if (eventSource) {
          eventSource.close();
        }
        reject(new Error(`Timeout: Did not receive '${eventName}' event within ${timeout / 1e3}s`));
      }, timeout);
      try {
        let headers = {};
        if (this.signer) {
          const mockRequest = new Request(url, { method: "GET" });
          const signedHeaders = await this.signer.sign(mockRequest);
          headers = { ...signedHeaders };
        }
        eventSource = new EventSource(url, { headers });
        eventSource.addEventListener(eventName, (event) => {
          clearTimeout(timeoutId);
          eventSource.close();
          try {
            const data = JSON.parse(event.data);
            resolve(data);
          } catch (e) {
            reject(new Error("Failed to parse event data"));
          }
        });
        eventSource.onerror = (err) => {
          clearTimeout(timeoutId);
          eventSource.close();
          reject(err || new Error("SSE connection error"));
        };
      } catch (err) {
        clearTimeout(timeoutId);
        reject(err);
      }
    });
  }
};

// src/utils/env.mjs
var import_os2 = __toESM(require("os"), 1);
var import_path2 = __toESM(require("path"), 1);
var import_dotenv = __toESM(require_main(), 1);

// src/utils/paths.mjs
var import_os = __toESM(require("os"), 1);
var import_path = __toESM(require("path"), 1);
var AGENTAUTH_ENV_PATH = import_path.default.join(import_os.default.homedir(), ".openclaw", ".env");

// src/utils/env.mjs
(0, import_dotenv.config)({ quiet: true });
var { parsed } = (0, import_dotenv.config)({ path: AGENTAUTH_ENV_PATH, quiet: true, override: true });
var ALLOWED_IDGW_BASE_URL_PATTERNS = [
  /^https:\/\/([a-zA-Z0-9-]+\.)*agentauth\.id/,
  /^http:\/\/localhost:\d+/
];
var Config = class {
  constructor(env = parsed || {}, ambientEnv = process.env) {
    this._env = env;
    this._ambientEnv = ambientEnv;
  }
  get openClawDir() {
    if (this._ambientEnv.OPENCLAW_STATE_DIR) {
      return this._ambientEnv.OPENCLAW_STATE_DIR;
    }
    const home = this._ambientEnv.OPENCLAW_HOME || import_os2.default.homedir();
    return import_path2.default.join(home, ".openclaw");
  }
  get idgwBaseUrl() {
    const baseUrl = this._ambientEnv.IDGW_BASE_URL || "https://consent.agentauth.id/api";
    const isAllowed = ALLOWED_IDGW_BASE_URL_PATTERNS.some(
      (pattern) => pattern.test(baseUrl)
    );
    if (!isAllowed) {
      throw new Error(
        `IDGW_BASE_URL "${baseUrl}" is not in the list of allowed origins. Allowed origin patterns are: https://<ENV>.agentauth.id, https://agentauth.id, http://localhost:<PORT>.`
      );
    }
    return baseUrl;
  }
  get notify() {
    return this._env.AGENTAUTH_NOTIFY;
  }
  get notificationChannel() {
    return this._ambientEnv.AGENTAUTH_NOTIFICATION_CHANNEL;
  }
  get hasCredentials() {
    return !!this._env.AGENTAUTH_API_KEY && !!this._env.AGENTAUTH_AGENT_KEY_ID;
  }
  get apiKey() {
    const apiKey = this._env.AGENTAUTH_API_KEY;
    if (!apiKey) {
      throw new Error(
        "Missing required environment variable: AGENTAUTH_API_KEY. Set it in your environment or .env file."
      );
    }
    return apiKey;
  }
  getAgentPrivateKey() {
    const pem = this._env.AGENTAUTH_AGENT_PRIVATE_KEY;
    if (!pem) {
      return;
    }
    return pem.replace(/\\n/g, "\n");
  }
  getAgentKeyId() {
    const keyId = this._env.AGENTAUTH_AGENT_KEY_ID;
    if (!keyId) {
      throw new Error(
        "Missing required environment variable: AGENTAUTH_AGENT_KEY_ID. Set it in your environment or .env file to enable request signing."
      );
    }
    return keyId;
  }
};
var config = new Config();

// src/services/NotificationService.mjs
var import_child_process = require("child_process");
var NotificationService = class {
  notify(message, channel, target) {
    throw new Error("notify() must be implemented");
  }
};
var OpenClawNotificationService = class extends NotificationService {
  notify(message, channel, target) {
    try {
      const args = ["message", "send", "--channel", channel, "--message", message];
      if (target) {
        args.push("--target", target);
      }
      (0, import_child_process.execFileSync)("openclaw", args, { stdio: "ignore" });
      return true;
    } catch (error) {
      console.error(`Failed to send message via OpenClaw: ${error.message}..`);
      return false;
    }
  }
};
var ConsoleNotificationService = class extends NotificationService {
  notify(message, channel, target) {
    console.log("[NOTIFICATION]");
    console.log(`Channel: ${channel}`);
    if (target) {
      console.log(`Target: ${target}`);
    }
    console.log(`Message: ${message}`);
    return true;
  }
};

// src/services/loginid/index.mjs
var import_crypto2 = require("crypto");

// src/services/loginid/queries.mjs
var APPROVAL_INIT_QUERY = `
  mutation approvalInit(
    $permissions: [PermissionInput!]!
  ) {
    approvalInit(
      permissions: $permissions
    ) {
      approvalUrl
      topic
    }
  }
`;
var ONBOARDING_INIT_QUERY = `
  mutation onboardingInit {
    onboardingInit {
      topic
      link
      agentId
    }
  }
`;

// src/services/loginid/index.mjs
var LoginIDService = class {
  #httpClient;
  #sseClient;
  #gqlUrl = "";
  #eventsUrl = "";
  #apiKey;
  #keyId;
  constructor({ baseUrl, httpClient, sseClient, credentials }) {
    this.#httpClient = httpClient;
    this.#sseClient = sseClient;
    this.#gqlUrl = baseUrl + "/graphql";
    this.#eventsUrl = baseUrl + "/events";
    this.#apiKey = credentials?.apiKey;
    this.#keyId = credentials?.keyId;
  }
  async createAuthSession() {
    const requestPayload = {
      operationName: "onboardingInit",
      query: ONBOARDING_INIT_QUERY
    };
    const { data } = await this.#httpClient.post(this.#gqlUrl, requestPayload);
    const result = data?.onboardingInit;
    if (!result) {
      throw new Error("Missing response data at `onboardingInit`");
    }
    return result;
  }
  async approvalInit(toolCall, displayString) {
    const requestPayload = {
      operationName: "approvalInit",
      query: APPROVAL_INIT_QUERY,
      variables: {
        permissions: [{
          id: (0, import_crypto2.randomUUID)(),
          title: toolCall,
          description: displayString
        }]
      }
    };
    const headers = {};
    if (this.#apiKey) {
      headers["X-Api-Key"] = this.#apiKey;
    }
    if (this.#keyId) {
      headers["X-Api-Key-Id"] = this.#keyId;
    }
    const { data } = await this.#httpClient.post(this.#gqlUrl, requestPayload, { headers });
    const result = data?.approvalInit;
    if (!result) {
      throw new Error("Missing response data at `approvalInit");
    }
    return result;
  }
  async waitForSession(topic) {
    const url = `${this.#eventsUrl}?topic=${topic}`;
    return await this.#sseClient.waitForEvent(
      url,
      { eventName: "session", timeout: 6e4 * 5 }
    );
  }
};

// src/utils/EnvManager.mjs
var import_path3 = __toESM(require("path"), 1);
var import_promises3 = __toESM(require("fs/promises"), 1);

// src/utils/agentMarkdown.mjs
var AGENTAUTH_PROMPT_VERSION = "1.0.0";
var AGENTAUTH_MD_ADDITION = `<!-- AGENTAUTH-START -->
<!-- AGENTAUTH-PROMPT-VERSION: ${AGENTAUTH_PROMPT_VERSION} -->
## Security (AgentAuth)

### Red Lines
If a dangerous action is requested (delete files, send email, modify config, purchases, production changes), use the agentauth skill for passkey approval before executing.

### Dangerous Operations Definition

Treat the following as **dangerous**:

* File deletions (\`rm\`, \`rm -rf\`, recursive deletes)
* System-level modifications
* Database destructive queries (\`DELETE\`, \`DROP\`, \`TRUNCATE\`)
* Production deployments or config changes
* External system writes (APIs, PR merges, emails)
* Security or permission changes
* Package installs or system mutations
* Modifying this file (AGENTS.md) to protect against unwanted rewrites.
* Any modification, deletion, or overwriting of the OpenClaw environment file (e.g. ~/.openclaw/.env).
* Any modification, deletion, or overwriting of the skills directory or its contents (e.g. ~/.openclaw/workspace/skills/agentauth).

If unsure \u2192 **assume dangerous**

### Tool
* **agentauth** \u2014 Human consent gate using passkeys to authorize sensitive actions.
<!-- AGENTAUTH-END -->`;
var ASK_FIRST_HEADER = `**Ask first:**`;
var ASK_FIRST_LIST = `- Sending emails, tweets, public posts
- Anything that leaves the machine
- Anything you're uncertain about`;
var ASK_FIRST_BLOCK = `${ASK_FIRST_HEADER}

${ASK_FIRST_LIST}`;

// src/utils/EnvManager.mjs
var EnvManager = class {
  #openClawDir;
  constructor({ openClawDir }) {
    this.#openClawDir = openClawDir;
  }
  async saveCredentials(keyId, apiKey) {
    const envPath = import_path3.default.join(this.#openClawDir, ".env");
    let envContent = "";
    try {
      envContent = await import_promises3.default.readFile(envPath, "utf8");
    } catch (error) {
      if (error.code !== "ENOENT") {
        throw error;
      }
    }
    const lines = envContent.split("\n");
    const otherLines = lines.filter(
      (line) => !line.startsWith("AGENTAUTH_AGENT_KEY_ID=") && !line.startsWith("AGENTAUTH_API_KEY=") && line.trim() !== ""
    );
    const newLines = [
      ...otherLines,
      `AGENTAUTH_AGENT_KEY_ID="${keyId}"`,
      `AGENTAUTH_API_KEY="${apiKey}"`
    ];
    try {
      await import_promises3.default.writeFile(envPath, newLines.join("\n") + "\n", { encoding: "utf8" });
    } catch (error) {
      throw new Error(`Could not save credentials to OpenClaw environment file at ${envPath}: ${error.message}`);
    }
  }
  async updateAgentMarkdown() {
    const agentMdPath = import_path3.default.join(this.#openClawDir, "workspace", "AGENTS.md");
    try {
      let content;
      try {
        content = await import_promises3.default.readFile(agentMdPath, "utf8");
      } catch (error) {
        if (error.code === "ENOENT") {
          console.warn(`[WARN] Could not update AGENTS.md: AGENTS.md could not be found`);
          return;
        }
        throw error;
      }
      const originalContent = content;
      const startMarker = "<!-- AGENTAUTH-START -->";
      const endMarker = "<!-- AGENTAUTH-END -->";
      const versionRegex = /<!-- AGENTAUTH-PROMPT-VERSION: (.*?) -->/;
      const newVersionMatch = AGENTAUTH_MD_ADDITION.match(versionRegex);
      const newVersion = newVersionMatch ? newVersionMatch[1] : null;
      const startIndex = content.indexOf(startMarker);
      const endIndex = content.indexOf(endMarker, startIndex);
      let newContent = content;
      if (startIndex !== -1 && endIndex !== -1) {
        const blockEndIndex = endIndex + endMarker.length;
        const existingBlock = content.substring(startIndex, blockEndIndex);
        const existingVersionMatch = existingBlock.match(versionRegex);
        const existingVersion = existingVersionMatch ? existingVersionMatch[1] : null;
        if (existingVersion !== newVersion) {
          newContent = content.substring(0, startIndex) + AGENTAUTH_MD_ADDITION + content.substring(blockEndIndex);
        }
      } else {
        newContent = (content.trim() ? content.trimEnd() + "\n\n" : "") + AGENTAUTH_MD_ADDITION;
      }
      newContent = this.#removeAskFirstBlock(newContent);
      if (originalContent !== newContent) {
        await import_promises3.default.writeFile(agentMdPath, newContent.trimEnd() + "\n", "utf8");
      }
    } catch (error) {
      if (error.code !== "ENOENT") {
        console.warn(`[WARN] Could not update AGENTS.md: ${error.message}`);
      }
    }
  }
  #removeAskFirstBlock(content) {
    const askFirstIndex = content.indexOf(ASK_FIRST_HEADER);
    if (askFirstIndex === -1) {
      return content;
    }
    const bodyStart = askFirstIndex + ASK_FIRST_HEADER.length;
    const nextHeadingMatch = content.slice(bodyStart).match(/\n##\s+/);
    let blockEndIndex;
    if (nextHeadingMatch) {
      blockEndIndex = bodyStart + nextHeadingMatch.index;
    } else {
      blockEndIndex = content.length;
    }
    const before = content.slice(0, askFirstIndex).trimEnd();
    const after = content.slice(blockEndIndex).trimStart();
    return [before, after].filter(Boolean).join("\n\n");
  }
  async restoreAgentMarkdown() {
    const agentMdPath = import_path3.default.join(this.#openClawDir, "workspace", "AGENTS.md");
    try {
      let content;
      try {
        content = await import_promises3.default.readFile(agentMdPath, "utf8");
      } catch (error) {
        if (error.code === "ENOENT") {
          return;
        }
        throw error;
      }
      if (content.includes(ASK_FIRST_HEADER)) {
        return;
      }
      const externalVsInternalHeader = "## External vs Internal";
      const sectionIndex = content.indexOf(externalVsInternalHeader);
      if (sectionIndex === -1) {
        console.warn(`[WARN] Could not restore "Ask first" block: "${externalVsInternalHeader}" section not found in AGENTS.md`);
        return;
      }
      const bodyStart = sectionIndex + externalVsInternalHeader.length;
      const nextHeadingMatch = content.slice(bodyStart).match(/^\s*##\s+/m);
      let insertionIndex;
      if (nextHeadingMatch) {
        insertionIndex = bodyStart + nextHeadingMatch.index;
      } else {
        insertionIndex = content.length;
      }
      const before = content.substring(0, insertionIndex).trimEnd();
      const after = content.substring(insertionIndex).trimStart();
      const newContent = [before, ASK_FIRST_BLOCK, after].filter(Boolean).join("\n\n");
      if (content !== newContent) {
        await import_promises3.default.writeFile(agentMdPath, newContent.trimEnd() + "\n", "utf8");
      }
    } catch (error) {
      console.warn(`[WARN] Could not update AGENTS.md: ${error.message}`);
    }
  }
};

// src/services/CommandExecutor.mjs
var import_child_process2 = require("child_process");
var CommandExecutor = class {
  async execute(command) {
    return new Promise((resolve) => {
      (0, import_child_process2.exec)(command, (error, stdout, stderr) => {
        if (error) {
          resolve({ error, stdout, stderr });
        } else {
          resolve({ error: null, stdout, stderr });
        }
      });
    });
  }
};

// src/cli/router.mjs
var notificationService = config.notificationChannel === "stdio" ? new ConsoleNotificationService() : new OpenClawNotificationService();
var envManager = new EnvManager({ openClawDir: config.openClawDir });
var commandExecutor = new CommandExecutor();
var getUnauthenticatedIdgwService = () => {
  const httpClient = new HttpClient();
  const sseClient = new SseClient();
  const loginIdService = new LoginIDService({
    baseUrl: config.idgwBaseUrl,
    httpClient,
    sseClient
  });
  return new IdentityGateWay({
    loginIdService,
    notificationService,
    envManager,
    commandExecutor,
    config
  });
};
var idgwService;
var getIdgwService = () => {
  if (idgwService) {
    return idgwService;
  }
  const apiKey = config.apiKey;
  const keyId = config.getAgentKeyId();
  const privateKey = config.getAgentPrivateKey();
  let signer;
  if (privateKey) {
    signer = new AgentSigner(privateKey, keyId);
  }
  const httpClient = new HttpClient({ signer });
  const sseClient = new SseClient();
  const loginIdService = new LoginIDService({
    baseUrl: config.idgwBaseUrl,
    httpClient,
    sseClient,
    credentials: { apiKey, keyId }
  });
  idgwService = new IdentityGateWay({
    loginIdService,
    notificationService,
    envManager,
    commandExecutor,
    config
  });
  return idgwService;
};
var commandFactories = {
  "auth-flow": () => new AuthFlowCommand(getUnauthenticatedIdgwService()),
  "approval-flow": () => new ApprovalFlowCommand(getIdgwService()),
  "test-notify": () => new TestNotifyCommand(notificationService),
  "cleanup": () => new CleanupCommand(getIdgwService())
};
function getCommand(commandName) {
  const factory = commandFactories[commandName];
  if (!factory) {
    throw new Error(`Command not found: ${commandName}`);
  }
  return factory();
}

// src/cli/main.mjs
var program2 = new Command();
program2.name("agentauth").description("A CLI tool for AgentAuths's Identity Gateway with OpenClaw").version("0.0.1");
program2.command("auth-flow").description("Starts an authentication flow for onboarding and waits for it to complete").option(
  "--notify <provider:destination>",
  "Send notification (e.g. telegram:@mychat, slack:channel:C123, whatsapp:+123...)"
).action(async (options) => {
  try {
    const command = getCommand("auth-flow");
    const { notify } = options;
    const result = await command.execute({ notify: notify || config.notify });
    if (result) {
      console.log(JSON.stringify(result));
    }
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
});
program2.command("approval-flow").description("Starts an approval flow and waits for it to complete").argument("<toolCall>", "the exact dangerous command or tool call that would be executed").argument("<displayString>", "a concise human-readable summary of the dangerous action for the approval UI").option(
  "--notify <provider:destination>",
  "Send notification (e.g. telegram:@mychat, slack:channel:C123, whatsapp:+123...)"
).action(async (toolCall, displayString, options) => {
  try {
    const command = getCommand("approval-flow");
    const { notify } = options;
    const result = await command.execute({ toolCall, displayString, notify: notify || config.notify });
    if (result) {
      console.log(JSON.stringify(result));
    }
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
});
program2.command("test-notify").description("Sends a test notification via OpenClaw to verify the message API is working.").argument("<message>", "The message to send").option(
  "--notify <provider:destination>",
  "Send notification (e.g. telegram:@mychat, slack:channel:C123, whatsapp:+123...)"
).action(async (message, options) => {
  try {
    const { notify } = options;
    const notifyValue = notify || config.notify;
    if (!notifyValue) {
      throw new Error(
        "missing required option '--notify <provider:destination>' or AGENTAUTH_NOTIFY environment variable."
      );
    }
    const command = getCommand("test-notify");
    await command.execute({ message, notify: notifyValue });
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
});
program2.command("cleanup").description("Restores original configuration and removes AgentAuth integrations. Run before uninstalling the AgentAuth skill.").option(
  "--notify <provider:destination>",
  "Send notification (e.g. telegram:@mychat, slack:channel:C123, whatsapp:+123...)"
).action(async (options) => {
  try {
    const command = getCommand("cleanup");
    const { notify } = options;
    await command.execute({ notify: notify || config.notify });
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
});
program2.parse();
