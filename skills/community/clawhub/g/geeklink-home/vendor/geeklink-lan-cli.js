#!/usr/bin/env node
"use strict";
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
    var childProcess = require("node:child_process");
    var path = require("node:path");
    var fs = require("node:fs");
    var process2 = require("node:process");
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
          writeOut: (str) => process2.stdout.write(str),
          writeErr: (str) => process2.stderr.write(str),
          outputError: (str, write) => write(str),
          getOutHelpWidth: () => process2.stdout.isTTY ? process2.stdout.columns : void 0,
          getErrHelpWidth: () => process2.stderr.isTTY ? process2.stderr.columns : void 0,
          getOutHasColors: () => useColor() ?? (process2.stdout.isTTY && process2.stdout.hasColors?.()),
          getErrHasColors: () => useColor() ?? (process2.stderr.isTTY && process2.stderr.hasColors?.()),
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
        process2.exit(exitCode);
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
      _optionEx(config, flags, description, fn, defaultValue) {
        if (typeof flags === "object" && flags instanceof Option2) {
          throw new Error(
            "To add an Option object use addOption() instead of option() or requiredOption()"
          );
        }
        const option = this.createOption(flags, description);
        option.makeOptionMandatory(!!config.mandatory);
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
          if (process2.versions?.electron) {
            parseOptions.from = "electron";
          }
          const execArgv = process2.execArgv ?? [];
          if (execArgv.includes("-e") || execArgv.includes("--eval") || execArgv.includes("-p") || execArgv.includes("--print")) {
            parseOptions.from = "eval";
          }
        }
        if (argv === void 0) {
          argv = process2.argv;
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
            if (process2.defaultApp) {
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
        if (fs.existsSync(executableFile)) return;
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
          const localBin = path.resolve(baseDir, baseName);
          if (fs.existsSync(localBin)) return localBin;
          if (sourceExt.includes(path.extname(baseName))) return void 0;
          const foundExt = sourceExt.find(
            (ext) => fs.existsSync(`${localBin}${ext}`)
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
            resolvedScriptPath = fs.realpathSync(this._scriptPath);
          } catch {
            resolvedScriptPath = this._scriptPath;
          }
          executableDir = path.resolve(
            path.dirname(resolvedScriptPath),
            executableDir
          );
        }
        if (executableDir) {
          let localFile = findFile(executableDir, executableFile);
          if (!localFile && !subcommand._executableFile && this._scriptPath) {
            const legacyName = path.basename(
              this._scriptPath,
              path.extname(this._scriptPath)
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
        launchWithNode = sourceExt.includes(path.extname(executableFile));
        let proc;
        if (process2.platform !== "win32") {
          if (launchWithNode) {
            args.unshift(executableFile);
            args = incrementNodeInspectorPort(process2.execArgv).concat(args);
            proc = childProcess.spawn(process2.argv[0], args, { stdio: "inherit" });
          } else {
            proc = childProcess.spawn(executableFile, args, { stdio: "inherit" });
          }
        } else {
          this._checkForMissingExecutable(
            executableFile,
            executableDir,
            subcommand._name
          );
          args.unshift(executableFile);
          args = incrementNodeInspectorPort(process2.execArgv).concat(args);
          proc = childProcess.spawn(process2.execPath, args, { stdio: "inherit" });
        }
        if (!proc.killed) {
          const signals = ["SIGUSR1", "SIGUSR2", "SIGTERM", "SIGINT", "SIGHUP"];
          signals.forEach((signal) => {
            process2.on(signal, () => {
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
            process2.exit(code);
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
            process2.exit(1);
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
        const parsed = this.parseOptions(unknown);
        this._parseOptionsEnv();
        this._parseOptionsImplied();
        operands = operands.concat(parsed.operands);
        unknown = parsed.unknown;
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
        this._outputHelpIfRequested(parsed.unknown);
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        const checkForUnknownOptions = () => {
          if (parsed.unknown.length > 0) {
            this.unknownOption(parsed.unknown[0]);
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
        const config = errorOptions || {};
        const exitCode = config.exitCode || 1;
        const code = config.code || "commander.error";
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
          if (option.envVar && option.envVar in process2.env) {
            const optionKey = option.attributeName();
            if (this.getOptionValue(optionKey) === void 0 || ["default", "config", "env"].includes(
              this.getOptionValueSource(optionKey)
            )) {
              if (option.required || option.optional) {
                this.emit(`optionEnv:${option.name()}`, process2.env[option.envVar]);
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
        this._name = path.basename(filename, path.extname(filename));
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
      executableDir(path2) {
        if (path2 === void 0) return this._executableDir;
        this._executableDir = path2;
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
        let exitCode = Number(process2.exitCode ?? 0);
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
      if (process2.env.NO_COLOR || process2.env.FORCE_COLOR === "0" || process2.env.FORCE_COLOR === "false")
        return false;
      if (process2.env.FORCE_COLOR || process2.env.CLICOLOR_FORCE !== void 0)
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

// src/utils.ts
function normalizeBaseUrl(host) {
  const trimmed = host.trim();
  if (!trimmed) {
    throw new Error("Gateway host is required");
  }
  if (/^https?:\/\//i.test(trimmed)) {
    return trimmed.replace(/\/+$/, "");
  }
  return `http://${trimmed.replace(/\/+$/, "")}`;
}
function printJson(data) {
  process.stdout.write(`${JSON.stringify(data, null, 2)}
`);
}
function isObject(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
function unixTimeNow() {
  return Math.floor(Date.now() / 1e3);
}
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// src/client.ts
var API_BASE = "/api/llm-skill/v1";
var GatewayApiError = class extends Error {
  status;
  body;
  constructor(message, status, body) {
    super(message);
    this.name = "GatewayApiError";
    this.status = status;
    this.body = body;
  }
};
var GatewayClient = class {
  baseUrl;
  sessionToken;
  constructor(host, sessionToken) {
    this.baseUrl = normalizeBaseUrl(host);
    this.sessionToken = sessionToken;
  }
  setSessionToken(token) {
    this.sessionToken = token;
  }
  async hello() {
    return this.requestJson("GET", "/hello");
  }
  async manifest() {
    return this.requestJson("GET", "/manifest");
  }
  async openapi() {
    return this.requestJson("GET", "/openapi.json");
  }
  async authExchange(pairingToken, clientName) {
    return this.requestJson("POST", "/auth/exchange", {
      pairing_token: pairingToken,
      client_name: clientName
    });
  }
  async catalogLlm() {
    return this.requestJson("GET", "/catalog/llm", void 0, true);
  }
  async catalogDevices() {
    return this.requestJson("GET", "/catalog/devices", void 0, true);
  }
  async catalogScenes() {
    return this.requestJson("GET", "/catalog/scenes", void 0, true);
  }
  async sceneDetail(sceneId) {
    return this.requestJson("GET", `/catalog/scenes/${sceneId}`, void 0, true);
  }
  async activateScene(sceneId) {
    return this.requestJson("POST", "/scene/activate", { scene_id: sceneId }, true);
  }
  async deviceControl(deviceId, payload) {
    return this.requestJson(
      "POST",
      "/device/control",
      {
        catalog_device_id: deviceId,
        ...payload
      },
      true
    );
  }
  async stateSnapshot() {
    return this.requestJson("GET", "/state/snapshot", void 0, true);
  }
  async stateChanges(sinceVersion, waitSec) {
    return this.requestJson(
      "GET",
      `/state/changes?since=${encodeURIComponent(String(sinceVersion))}&wait=${encodeURIComponent(String(waitSec))}`,
      void 0,
      true,
      (waitSec + 10) * 1e3
    );
  }
  async requestJson(method, path, body, withAuth = false, timeoutMs = 15e3) {
    const headers = {
      Accept: "application/json"
    };
    if (body !== void 0) {
      headers["Content-Type"] = "application/json";
    }
    if (withAuth) {
      if (!this.sessionToken) {
        throw new Error("Session token is required for this request");
      }
      headers.Authorization = `Bearer ${this.sessionToken}`;
    }
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetch(`${this.baseUrl}${API_BASE}${path}`, {
        method,
        headers,
        body: body !== void 0 ? JSON.stringify(body) : void 0,
        signal: controller.signal
      });
      const text = await response.text();
      const parsed = text ? this.tryParseJson(text) : void 0;
      if (!response.ok) {
        const message = this.extractErrorMessage(parsed) ?? response.statusText ?? "Gateway request failed";
        throw new GatewayApiError(message, response.status, parsed);
      }
      if (parsed === void 0) {
        throw new GatewayApiError("Gateway returned empty response", response.status);
      }
      return parsed;
    } catch (error) {
      if (error instanceof GatewayApiError) {
        throw error;
      }
      if (error.name === "AbortError") {
        throw new Error(`Gateway request timeout after ${timeoutMs} ms`);
      }
      throw error;
    } finally {
      clearTimeout(timer);
    }
  }
  tryParseJson(text) {
    try {
      return JSON.parse(text);
    } catch {
      return { raw: text };
    }
  }
  extractErrorMessage(body) {
    if (body && typeof body === "object" && "error" in body) {
      const value = body.error;
      if (typeof value === "string" && value) {
        return value;
      }
    }
    return void 0;
  }
};

// src/config.ts
var import_node_fs = require("node:fs");
var import_node_path = require("node:path");
var import_node_os = require("node:os");
var DEFAULT_CONFIG_DIR = (0, import_node_path.join)((0, import_node_os.homedir)(), ".geeklink-home");
var DEFAULT_CONFIG_PATH = (0, import_node_path.join)(DEFAULT_CONFIG_DIR, "config.json");
function getDefaultConfigPath() {
  return DEFAULT_CONFIG_PATH;
}
function loadConfig(configPath = DEFAULT_CONFIG_PATH) {
  if (!(0, import_node_fs.existsSync)(configPath)) {
    return {};
  }
  try {
    const raw = (0, import_node_fs.readFileSync)(configPath, "utf8");
    const parsed = JSON.parse(raw);
    return parsed ?? {};
  } catch (error) {
    throw new Error(`Failed to read config file ${configPath}: ${error.message}`);
  }
}
function saveConfig(config, configPath = DEFAULT_CONFIG_PATH) {
  (0, import_node_fs.mkdirSync)((0, import_node_path.dirname)(configPath), { recursive: true });
  (0, import_node_fs.writeFileSync)(configPath, `${JSON.stringify(config, null, 2)}
`, "utf8");
}
function mergeConfig(base, override) {
  return {
    host: override.host ?? base.host,
    pairingToken: override.pairingToken ?? base.pairingToken,
    clientName: override.clientName ?? base.clientName,
    sessionToken: override.sessionToken ?? base.sessionToken,
    expiresAt: override.expiresAt ?? base.expiresAt
  };
}
function clearSession(config) {
  return {
    host: config.host,
    pairingToken: config.pairingToken,
    clientName: config.clientName
  };
}

// src/sdk.ts
function parseCatalogDeviceTarget(catalogDeviceId) {
  const trimmed = catalogDeviceId.trim();
  const match = /^(.*)#(\d+)$/.exec(trimmed);
  if (!match) {
    return { baseCatalogDeviceId: trimmed };
  }
  return {
    baseCatalogDeviceId: match[1],
    roadId: Number(match[2])
  };
}
function buildVirtualCatalogDeviceId(baseCatalogDeviceId, roadId) {
  return `${baseCatalogDeviceId}#${roadId}`;
}
function uniqStrings(values) {
  const seen = /* @__PURE__ */ new Set();
  const result = [];
  for (const value of values) {
    if (typeof value !== "string") {
      continue;
    }
    const trimmed = value.trim();
    if (!trimmed || seen.has(trimmed)) {
      continue;
    }
    seen.add(trimmed);
    result.push(trimmed);
  }
  return result;
}
function formatWatcherError(error) {
  if (error instanceof Error && error.message) {
    return error.message;
  }
  return String(error);
}
var RECENT_EVENTS_LIMIT = 64;
var LanLlmSkillSdk = class {
  configPath;
  autoPersistConfig;
  config;
  client;
  catalogCache;
  rawStateSnapshotCache;
  stateSnapshotCache;
  recentEvents = [];
  watcherStopSignal;
  watcherReadyPromise;
  watcherRunPromise;
  watcherStartedAt;
  watcherLastError;
  watcherCurrentVersion = 0;
  constructor(options) {
    this.configPath = options.configPath ?? getDefaultConfigPath();
    const diskConfig = loadConfig(this.configPath);
    this.config = mergeConfig(diskConfig, {
      host: options.host,
      pairingToken: options.pairingToken,
      clientName: options.clientName,
      sessionToken: options.sessionToken
    });
    if (!this.config.host) {
      throw new Error("Gateway host is required");
    }
    this.autoPersistConfig = options.autoPersistConfig ?? true;
    this.client = new GatewayClient(this.config.host, this.config.sessionToken);
  }
  getConfig() {
    return { ...this.config };
  }
  async hello() {
    return this.client.hello();
  }
  async manifest() {
    return this.client.manifest();
  }
  async openapi() {
    return this.client.openapi();
  }
  async login(pairingToken, clientName) {
    const token = pairingToken ?? this.config.pairingToken;
    const name = clientName ?? this.config.clientName ?? "nodejs-skill";
    if (!token) {
      throw new Error("Pairing token is required");
    }
    const auth = await this.client.authExchange(token, name);
    this.config = {
      ...this.config,
      pairingToken: token,
      clientName: auth.client_name,
      sessionToken: auth.session_token,
      expiresAt: auth.expires_at
    };
    this.client.setSessionToken(auth.session_token);
    this.persistConfig();
    return this.getConfig();
  }
  async ensureAuthorized() {
    if (this.config.sessionToken && this.config.expiresAt && this.config.expiresAt > unixTimeNow() + 30) {
      this.client.setSessionToken(this.config.sessionToken);
      return;
    }
    if (!this.config.pairingToken) {
      throw new Error("No valid session token and no pairing token available");
    }
    await this.login(this.config.pairingToken, this.config.clientName);
  }
  async refreshAuthorization() {
    if (!this.config.pairingToken) {
      throw new Error("No pairing token available for session refresh");
    }
    const auth = await this.client.authExchange(this.config.pairingToken, this.config.clientName ?? "nodejs-skill");
    this.config = {
      ...this.config,
      clientName: auth.client_name,
      sessionToken: auth.session_token,
      expiresAt: auth.expires_at
    };
    this.client.setSessionToken(auth.session_token);
    this.persistConfig();
  }
  async withAuthorizationRetry(fn) {
    await this.ensureAuthorized();
    try {
      return await fn();
    } catch (error) {
      const status = typeof error === "object" && error && "status" in error ? error.status : void 0;
      if (status !== 401 || !this.config.pairingToken) {
        throw error;
      }
      this.config = {
        ...this.config,
        sessionToken: void 0,
        expiresAt: void 0
      };
      this.client.setSessionToken(void 0);
      await this.refreshAuthorization();
      return fn();
    }
  }
  async getCatalogSnapshot(forceRefresh = false) {
    if (!forceRefresh && this.catalogCache) {
      return this.catalogCache;
    }
    const snapshot = await this.withAuthorizationRetry(() => this.client.catalogLlm());
    if (!isObject(snapshot)) {
      throw new Error("Invalid catalog snapshot");
    }
    this.catalogCache = snapshot;
    return this.catalogCache;
  }
  async listDevices(forceRefresh = false) {
    const snapshot = await this.getCatalogSnapshot(forceRefresh);
    return this.expandCatalogDevices(Array.isArray(snapshot.devices) ? snapshot.devices : []);
  }
  async listScenes(forceRefresh = false) {
    const snapshot = await this.getCatalogSnapshot(forceRefresh);
    return Array.isArray(snapshot.scenes) ? snapshot.scenes : [];
  }
  async getSceneDetail(sceneId) {
    return this.withAuthorizationRetry(() => this.client.sceneDetail(sceneId));
  }
  async activateScene(sceneId) {
    return this.withAuthorizationRetry(() => this.client.activateScene(sceneId));
  }
  async controlDevice(catalogDeviceId, payload) {
    const target = parseCatalogDeviceTarget(catalogDeviceId);
    const nextPayload = { ...payload };
    if (target.roadId !== void 0 && nextPayload.road_id === void 0) {
      nextPayload.road_id = target.roadId;
    }
    return this.withAuthorizationRetry(() => this.client.deviceControl(target.baseCatalogDeviceId, nextPayload));
  }
  async getStateSnapshot(forceRefresh = false) {
    if (!forceRefresh && this.stateSnapshotCache) {
      return this.stateSnapshotCache;
    }
    const rawSnapshot = await this.withAuthorizationRetry(() => this.client.stateSnapshot());
    const catalog = await this.getCatalogSnapshot(forceRefresh);
    const devices = Array.isArray(catalog.devices) ? catalog.devices : [];
    this.rawStateSnapshotCache = rawSnapshot;
    this.stateSnapshotCache = this.expandStateSnapshot(rawSnapshot, devices);
    this.watcherCurrentVersion = this.stateSnapshotCache.version;
    return this.stateSnapshotCache;
  }
  async findDevicesByQuery(query, forceRefresh = false) {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return [];
    }
    const devices = await this.listDevices(forceRefresh);
    const scored = devices.map((device) => ({
      device,
      score: this.matchDeviceScore(device, normalized)
    })).filter((item) => item.score > 0).sort((a, b) => b.score - a.score);
    return scored.map((item) => item.device);
  }
  async startWatcher(options = {}) {
    if (this.watcherReadyPromise) {
      await this.watcherReadyPromise;
      return this.getWatcherStatus();
    }
    const stopSignal = { stopped: false };
    let ready = false;
    let resolveReady = () => void 0;
    let rejectReady = () => void 0;
    this.watcherStartedAt = unixTimeNow();
    this.watcherLastError = void 0;
    this.watcherStopSignal = stopSignal;
    this.watcherReadyPromise = new Promise((resolve, reject) => {
      resolveReady = () => {
        if (ready) {
          return;
        }
        ready = true;
        resolve();
      };
      rejectReady = (error) => {
        if (ready) {
          return;
        }
        ready = true;
        reject(error);
      };
    });
    const runPromise = this.watchState({
      withSnapshot: options.withSnapshot ?? true,
      waitSec: options.waitSec,
      retryDelayMs: options.retryDelayMs,
      stopSignal,
      onSnapshot: async (snapshot) => {
        this.watcherCurrentVersion = snapshot.version;
        resolveReady();
      },
      onChanges: async () => {
        resolveReady();
      },
      onError: async (error) => {
        this.watcherLastError = formatWatcherError(error);
      }
    }).catch((error) => {
      this.watcherLastError = formatWatcherError(error);
      rejectReady(error);
      throw error;
    }).finally(() => {
      if (this.watcherRunPromise === runPromise) {
        this.watcherRunPromise = void 0;
        this.watcherReadyPromise = void 0;
        this.watcherStopSignal = void 0;
      }
    });
    this.watcherRunPromise = runPromise;
    void runPromise.catch(() => void 0);
    try {
      await this.watcherReadyPromise;
    } catch (error) {
      this.watcherLastError = formatWatcherError(error);
      throw error;
    }
    return this.getWatcherStatus();
  }
  async stopWatcher() {
    if (this.watcherStopSignal) {
      this.watcherStopSignal.stopped = true;
    }
    if (this.watcherRunPromise) {
      await this.watcherRunPromise.catch(() => void 0);
    }
  }
  isWatcherRunning() {
    return Boolean(this.watcherStopSignal && !this.watcherStopSignal.stopped && this.watcherRunPromise);
  }
  getWatcherStatus() {
    return {
      running: this.isWatcherRunning(),
      started_at: this.watcherStartedAt,
      current_version: this.watcherCurrentVersion || this.stateSnapshotCache?.version || 0,
      last_error: this.watcherLastError
    };
  }
  async getRecentEvents(options = {}) {
    if (options.startWatcher !== false) {
      await this.startWatcher();
    }
    let events = [...this.recentEvents];
    const types = Array.isArray(options.type) ? options.type : options.type ? [options.type] : void 0;
    if (types && types.length > 0) {
      const allowed = new Set(types);
      events = events.filter((event) => allowed.has(event.type));
    }
    if (options.deviceId) {
      events = events.filter((event) => event.device_id === options.deviceId || event.parent_device_id === options.deviceId);
    }
    const limit = Math.max(1, Math.min(options.limit ?? 20, RECENT_EVENTS_LIMIT));
    events = events.slice(-limit).reverse();
    return {
      ok: true,
      current_version: this.getWatcherStatus().current_version ?? 0,
      watcher: this.getWatcherStatus(),
      events
    };
  }
  async getDeviceState(catalogDeviceId, options = {}) {
    if (options.startWatcher !== false) {
      await this.startWatcher();
    }
    const snapshot = await this.getStateSnapshot(Boolean(options.refresh));
    const catalog = await this.getCatalogSnapshot(Boolean(options.refresh));
    const devices = Array.isArray(catalog.devices) ? this.expandCatalogDevices(catalog.devices) : [];
    return {
      ok: true,
      current_version: snapshot.version,
      watcher: this.getWatcherStatus(),
      device: snapshot.devices.find((item) => item.device_id === catalogDeviceId) ?? null,
      catalog_device: devices.find((item) => item.catalog_device_id === catalogDeviceId) ?? null
    };
  }
  async watchState(options = {}) {
    await this.ensureAuthorized();
    let version = options.since ?? 0;
    const waitSec = options.waitSec ?? 25;
    const retryDelayMs = options.retryDelayMs ?? 2e3;
    if (options.withSnapshot || version === 0) {
      const snapshot = await this.getStateSnapshot(true);
      version = snapshot.version;
      if (options.onSnapshot) {
        await options.onSnapshot(snapshot);
      }
    }
    while (!options.stopSignal?.stopped) {
      try {
        const changes = await this.withAuthorizationRetry(() => this.client.stateChanges(version, waitSec));
        if (changes.snapshot_required) {
          const snapshot = await this.getStateSnapshot(true);
          version = snapshot.version;
          if (options.onSnapshot) {
            await options.onSnapshot(snapshot);
          }
          continue;
        }
        const expandedChanges = await this.applyChangesAndUpdateCaches(changes);
        if (options.onChanges) {
          await options.onChanges(expandedChanges);
        }
        version = Math.max(version, expandedChanges.current_version);
      } catch (error) {
        if (options.onError) {
          await options.onError(error);
        }
        await new Promise((resolve) => setTimeout(resolve, retryDelayMs));
      }
    }
  }
  persistConfig() {
    if (!this.autoPersistConfig) {
      return;
    }
    saveConfig(this.config, this.configPath);
  }
  matchDeviceScore(device, normalized) {
    const fields = [];
    if (typeof device.catalog_device_id === "string") {
      fields.push(device.catalog_device_id);
    }
    if (typeof device.name === "string") {
      fields.push(device.name);
    }
    if (typeof device.display_name === "string") {
      fields.push(device.display_name);
    }
    if (typeof device.room_name === "string") {
      fields.push(device.room_name);
    }
    if (Array.isArray(device.aliases)) {
      fields.push(...device.aliases.filter((item) => typeof item === "string"));
    }
    let score = 0;
    for (const field of fields) {
      const value = field.trim().toLowerCase();
      if (!value) {
        continue;
      }
      if (value === normalized) {
        score = Math.max(score, 100);
      } else if (value.includes(normalized)) {
        score = Math.max(score, 60);
      }
    }
    return score;
  }
  applyChangesToSnapshot(snapshot, changes) {
    if (!snapshot) {
      return snapshot;
    }
    const map = new Map(snapshot.devices.map((device) => [device.device_id, { ...device }]));
    for (const event of changes.events) {
      if (event.type === "device.state" && event.device_id) {
        const current = map.get(event.device_id) ?? { device_id: event.device_id, updated_at: event.ts };
        current.updated_at = event.ts;
        if (event.online !== void 0) {
          current.online = event.online;
        }
        if (event.state) {
          current.state = event.state;
          delete current.state_raw;
        }
        if (event.state_raw) {
          current.state_raw = event.state_raw;
          delete current.state;
        }
        map.set(event.device_id, current);
      } else if (event.type === "device.online" && event.device_id) {
        const current = map.get(event.device_id) ?? { device_id: event.device_id, updated_at: event.ts };
        current.updated_at = event.ts;
        current.online = event.online;
        map.set(event.device_id, current);
      } else if (event.type === "device.removed" && event.device_id) {
        map.delete(event.device_id);
      }
    }
    return {
      ok: true,
      version: changes.current_version,
      devices: Array.from(map.values())
    };
  }
  async applyChangesAndUpdateCaches(changes) {
    const catalog = await this.getCatalogSnapshot(false);
    const devices = Array.isArray(catalog.devices) ? catalog.devices : [];
    this.rawStateSnapshotCache = this.applyChangesToSnapshot(this.rawStateSnapshotCache, changes);
    if (this.rawStateSnapshotCache) {
      this.stateSnapshotCache = this.expandStateSnapshot(this.rawStateSnapshotCache, devices);
    }
    const expandedChanges = this.expandStateChanges(changes, devices);
    this.recordRecentEvents(expandedChanges.events);
    this.watcherCurrentVersion = Math.max(this.watcherCurrentVersion, expandedChanges.current_version);
    return expandedChanges;
  }
  expandStateChanges(changes, devices) {
    return {
      ...changes,
      events: changes.events.flatMap((event) => this.expandStateEvent(event, devices))
    };
  }
  expandStateEvent(event, devices) {
    if (!event.device_id) {
      return [{ ...event }];
    }
    const catalogDevice = devices.find((device) => device.catalog_device_id === event.device_id);
    const baseEvent = {
      ...event,
      display_name: event.display_name ?? (typeof catalogDevice?.display_name === "string" ? catalogDevice.display_name : typeof catalogDevice?.name === "string" ? catalogDevice.name : void 0)
    };
    const roads = Array.isArray(catalogDevice?.roads) ? catalogDevice.roads.filter((road) => this.isValidRoad(road)) : [];
    if (roads.length <= 0) {
      return [baseEvent];
    }
    if (event.type === "device.online" || event.type === "device.removed") {
      return roads.map((road) => ({
        ...baseEvent,
        device_id: buildVirtualCatalogDeviceId(event.device_id, road.road_id),
        parent_device_id: event.device_id,
        road_id: road.road_id,
        road_name: road.name,
        display_name: this.buildRoadDisplayName(catalogDevice, road)
      }));
    }
    if (event.type !== "device.state" || !event.state || !isObject(event.state)) {
      return [baseEvent];
    }
    const expanded = [];
    for (const road of roads) {
      const roadValue = event.state[`road${road.road_id}`];
      if (typeof roadValue !== "boolean" && typeof roadValue !== "number") {
        continue;
      }
      expanded.push({
        ...baseEvent,
        device_id: buildVirtualCatalogDeviceId(event.device_id, road.road_id),
        parent_device_id: event.device_id,
        road_id: road.road_id,
        road_name: road.name,
        display_name: this.buildRoadDisplayName(catalogDevice, road),
        state: {
          power: Boolean(roadValue) ? "on" : "off",
          road_id: road.road_id,
          road_name: road.name,
          parent_device_id: event.device_id
        }
      });
    }
    return expanded.length > 0 ? expanded : [baseEvent];
  }
  recordRecentEvents(events) {
    if (events.length <= 0) {
      return;
    }
    this.recentEvents.push(...events.map((event) => ({ ...event })));
    if (this.recentEvents.length > RECENT_EVENTS_LIMIT) {
      this.recentEvents.splice(0, this.recentEvents.length - RECENT_EVENTS_LIMIT);
    }
  }
  expandCatalogDevices(devices) {
    const expanded = [];
    for (const device of devices) {
      const roads = Array.isArray(device.roads) ? device.roads.filter((road) => this.isValidRoad(road)) : [];
      if (roads.length <= 0) {
        expanded.push(device);
        continue;
      }
      for (const road of roads) {
        const parentName = typeof device.name === "string" ? device.name.trim() : "";
        const roadName = typeof road.name === "string" ? road.name.trim() : "";
        const displayName = this.buildRoadDisplayName(device, road);
        expanded.push({
          ...device,
          catalog_device_id: buildVirtualCatalogDeviceId(device.catalog_device_id, road.road_id),
          name: roadName || parentName,
          display_name: displayName || roadName || parentName,
          aliases: uniqStrings([
            roadName,
            displayName,
            device.room_name && roadName ? `${device.room_name}${roadName}` : void 0,
            parentName && roadName ? `${parentName} ${roadName}` : void 0,
            parentName && roadName ? `${parentName}${roadName}` : void 0,
            ...Array.isArray(device.aliases) ? device.aliases : []
          ]),
          parent_catalog_device_id: device.catalog_device_id,
          parent_name: parentName,
          road_id: road.road_id,
          is_virtual_road: true,
          capabilities: ["power"]
        });
      }
    }
    return expanded;
  }
  expandStateSnapshot(snapshot, devices) {
    return {
      ...snapshot,
      devices: snapshot.devices.flatMap((item) => this.expandStateSnapshotItem(item, devices))
    };
  }
  expandStateSnapshotItem(item, devices) {
    const catalogDevice = devices.find((device) => device.catalog_device_id === item.device_id);
    const roads = Array.isArray(catalogDevice?.roads) ? catalogDevice.roads.filter((road) => this.isValidRoad(road)) : [];
    if (roads.length <= 0 || !item.state || !isObject(item.state)) {
      return [item];
    }
    const expanded = [];
    for (const road of roads) {
      const roadValue = item.state?.[`road${road.road_id}`];
      if (typeof roadValue !== "boolean" && typeof roadValue !== "number") {
        continue;
      }
      expanded.push({
        device_id: buildVirtualCatalogDeviceId(item.device_id, road.road_id),
        updated_at: item.updated_at,
        online: item.online,
        state: {
          power: Boolean(roadValue) ? "on" : "off",
          road_id: road.road_id,
          road_name: road.name,
          parent_device_id: item.device_id
        }
      });
    }
    return expanded.length > 0 ? expanded : [item];
  }
  isValidRoad(road) {
    return typeof road.road_id === "number" && road.road_id > 0;
  }
  buildRoadDisplayName(device, road) {
    const roomName = typeof device.room_name === "string" ? device.room_name.trim() : "";
    const roadName = typeof road.name === "string" ? road.name.trim() : "";
    return uniqStrings([roomName, roadName]).join(" ");
  }
};

// src/openclaw.ts
function getOpenClawToolDefinitions() {
  return [
    {
      name: "geeklink_list_devices",
      description: "List Geeklink Home catalog devices available on the local gateway. Multi-gang switch panels are expanded into practical sub-devices such as \u540A\u706F or \u7B52\u706F.",
      inputSchema: {
        type: "object",
        properties: {
          refresh: { type: "boolean", description: "Refresh catalog from gateway before listing." },
          query: { type: "string", description: "Optional fuzzy filter by device name, room name, alias or device id." }
        }
      }
    },
    {
      name: "geeklink_list_scenes",
      description: "List Geeklink Home catalog scenes available on the local gateway.",
      inputSchema: {
        type: "object",
        properties: {
          refresh: { type: "boolean", description: "Refresh catalog from gateway before listing." }
        }
      }
    },
    {
      name: "geeklink_get_scene_detail",
      description: "Get the raw detail JSON for a scene by scene_id.",
      inputSchema: {
        type: "object",
        properties: {
          scene_id: { type: "integer", description: "Scene id from geeklink_list_scenes." }
        },
        required: ["scene_id"]
      }
    },
    {
      name: "geeklink_activate_scene",
      description: "Activate a scene by scene_id.",
      inputSchema: {
        type: "object",
        properties: {
          scene_id: { type: "integer", description: "Scene id from geeklink_list_scenes." }
        },
        required: ["scene_id"]
      }
    },
    {
      name: "geeklink_get_state_snapshot",
      description: "Get the latest runtime state snapshot from the local gateway.",
      inputSchema: {
        type: "object",
        properties: {
          refresh: { type: "boolean", description: "Refresh snapshot from gateway before returning." }
        }
      }
    },
    {
      name: "geeklink_get_device_state",
      description: "Get the latest known runtime state for one Geeklink Home device. Prefer catalog_device_id from geeklink_list_devices.",
      inputSchema: {
        type: "object",
        properties: {
          catalog_device_id: { type: "string", description: "Device id from geeklink_list_devices." },
          query: { type: "string", description: "Optional fuzzy lookup text. Use only when catalog_device_id is not available." },
          refresh: { type: "boolean", description: "Refresh snapshot from gateway before returning." }
        }
      }
    },
    {
      name: "geeklink_get_recent_events",
      description: "Get the most recent device and scene runtime events collected by the background watcher.",
      inputSchema: {
        type: "object",
        properties: {
          limit: { type: "integer", description: "Maximum number of recent events to return. Default 20." },
          device_id: { type: "string", description: "Optional catalog_device_id filter." },
          event_type: {
            type: "string",
            description: "Optional event type filter: device.state, device.online, device.removed, scene.executed, catalog.updated."
          }
        }
      }
    },
    {
      name: "geeklink_control_device",
      description: "Control a local Geeklink Home catalog device by catalog_device_id. Expanded multi-gang sub-devices returned by geeklink_list_devices are supported directly.",
      inputSchema: {
        type: "object",
        properties: {
          catalog_device_id: { type: "string", description: "Device id from geeklink_list_devices." },
          power: { type: ["boolean", "string"], description: "On/off or open/close semantic value." },
          brightness: { type: "integer", description: "Brightness 0..100 for light devices." },
          color_temp: { type: "integer", description: "Color temperature 0..100 for supported lights." },
          temperature: { type: "integer", description: "Target temperature 0..31 for temp control devices." },
          mode: { type: "string", description: "HVAC mode: auto/cool/dry/fan/fan_only/heat." },
          fan_speed: { type: "string", description: "Fan speed: auto/low/mid/medium/high." },
          action: { type: "string", description: "Curtain action: open/close/stop." },
          position: { type: "integer", description: "Curtain position 0..100." },
          value: { type: "string", description: "Legacy passthrough hex value." }
        },
        required: ["catalog_device_id"]
      }
    }
  ];
}
function ensureObject(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return {};
  }
  return input;
}
function getBoolean(input, key) {
  return Boolean(input[key]);
}
function getNumber(input, key) {
  const value = input[key];
  if (typeof value !== "number" || Number.isNaN(value)) {
    throw new Error(`${key} must be a number`);
  }
  return value;
}
function getString(input, key) {
  const value = input[key];
  if (typeof value !== "string" || !value.trim()) {
    throw new Error(`${key} must be a non-empty string`);
  }
  return value.trim();
}
function normalizeControlPayload(input) {
  const payload = {};
  const keys = ["power", "brightness", "temperature", "mode", "fan_speed", "action", "position", "value"];
  for (const key of keys) {
    if (input[key] !== void 0) {
      payload[key] = input[key];
    }
  }
  if (input.color_temp !== void 0) {
    payload.color_temp = input.color_temp;
  }
  return payload;
}
function parseEventType(value) {
  if (typeof value !== "string") {
    return void 0;
  }
  const trimmed = value.trim();
  switch (trimmed) {
    case "catalog.updated":
      return "catalog.updated";
    case "device.state":
      return "device.state";
    case "device.online":
      return "device.online";
    case "device.removed":
      return "device.removed";
    case "scene.executed":
      return "scene.executed";
    default:
      throw new Error("event_type must be one of: catalog.updated, device.state, device.online, device.removed, scene.executed");
  }
}
var OpenClawToolAdapter = class {
  sdk;
  watcherJoinPromise;
  persistentWatcher;
  constructor(options) {
    this.sdk = new LanLlmSkillSdk(options);
    this.persistentWatcher = options.persistentWatcher ?? false;
  }
  getToolDefinitions() {
    return getOpenClawToolDefinitions();
  }
  async executeTool(name, rawInput) {
    const input = ensureObject(rawInput);
    if (this.persistentWatcher && name !== "geeklink_list_scenes" && name !== "geeklink_get_scene_detail" && name !== "geeklink_activate_scene") {
      await this.ensureWatcherStarted();
    }
    switch (name) {
      case "geeklink_list_devices":
        return {
          ok: true,
          tool: name,
          output: await this.handleListDevices(input)
        };
      case "geeklink_list_scenes":
        return {
          ok: true,
          tool: name,
          output: await this.sdk.listScenes(getBoolean(input, "refresh"))
        };
      case "geeklink_get_scene_detail":
        return {
          ok: true,
          tool: name,
          output: await this.sdk.getSceneDetail(getNumber(input, "scene_id"))
        };
      case "geeklink_activate_scene":
        return {
          ok: true,
          tool: name,
          output: await this.sdk.activateScene(getNumber(input, "scene_id"))
        };
      case "geeklink_get_state_snapshot":
        return {
          ok: true,
          tool: name,
          output: await this.sdk.getStateSnapshot(getBoolean(input, "refresh"))
        };
      case "geeklink_get_device_state":
        return {
          ok: true,
          tool: name,
          output: await this.handleGetDeviceState(input)
        };
      case "geeklink_get_recent_events":
        return {
          ok: true,
          tool: name,
          output: await this.handleGetRecentEvents(input)
        };
      case "geeklink_control_device":
        return {
          ok: true,
          tool: name,
          output: await this.handleControlDevice(input)
        };
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  }
  async handleListDevices(input) {
    const refresh = getBoolean(input, "refresh");
    const query = typeof input.query === "string" ? input.query.trim() : "";
    if (query) {
      return this.sdk.findDevicesByQuery(query, refresh);
    }
    return this.sdk.listDevices(refresh);
  }
  async handleControlDevice(input) {
    const catalogDeviceId = getString(input, "catalog_device_id");
    const payload = normalizeControlPayload(input);
    delete payload.catalog_device_id;
    if (!Object.keys(payload).length) {
      throw new Error("geeklink_control_device requires at least one control field");
    }
    return this.sdk.controlDevice(catalogDeviceId, payload);
  }
  async startWatcher() {
    await this.ensureWatcherStarted();
  }
  async ensureWatcherStarted() {
    if (this.sdk.isWatcherRunning()) {
      return;
    }
    if (!this.watcherJoinPromise) {
      this.watcherJoinPromise = this.sdk.startWatcher({ withSnapshot: true }).then(() => void 0).finally(() => {
        this.watcherJoinPromise = void 0;
      });
    }
    await this.watcherJoinPromise;
  }
  async handleGetDeviceState(input) {
    const refresh = getBoolean(input, "refresh");
    const catalogDeviceId = typeof input.catalog_device_id === "string" ? input.catalog_device_id.trim() : "";
    const query = typeof input.query === "string" ? input.query.trim() : "";
    if (catalogDeviceId) {
      return this.sdk.getDeviceState(catalogDeviceId, this.buildDeviceStateOptions(refresh));
    }
    if (!query) {
      throw new Error("geeklink_get_device_state requires catalog_device_id or query");
    }
    const matches = await this.sdk.findDevicesByQuery(query, refresh);
    if (matches.length <= 0) {
      return {
        ok: false,
        error: "device_not_found",
        query,
        matches: []
      };
    }
    if (matches.length > 1) {
      return {
        ok: false,
        error: "device_query_ambiguous",
        query,
        matches: matches.slice(0, 5)
      };
    }
    return this.sdk.getDeviceState(matches[0].catalog_device_id, this.buildDeviceStateOptions(refresh));
  }
  async handleGetRecentEvents(input) {
    const limit = input.limit === void 0 ? void 0 : getNumber(input, "limit");
    const eventType = parseEventType(input.event_type);
    const deviceId = typeof input.device_id === "string" ? input.device_id.trim() : void 0;
    return this.sdk.getRecentEvents({
      limit,
      deviceId,
      type: eventType,
      startWatcher: this.persistentWatcher
    });
  }
  buildDeviceStateOptions(refresh) {
    return {
      refresh,
      startWatcher: this.persistentWatcher
    };
  }
};

// src/skill_runtime.ts
var GEEKLINK_HOME_SKILL_PROMPT = `\u4F60\u662F\u4E00\u4E2A\u8FD0\u884C\u5728\u5C40\u57DF\u7F51\u73AF\u5883\u4E2D\u7684\u5BB6\u5EAD\u8BBE\u5907\u52A9\u624B\u3002\u4F60\u901A\u8FC7 Geeklink Home Skill \u4E0E\u672C\u5730\u7F51\u5173\u901A\u4FE1\uFF0C\u8D1F\u8D23\u8BFB\u53D6\u8BBE\u5907\u5217\u8868\u3001\u573A\u666F\u5217\u8868\u3001\u8BBE\u5907\u72B6\u6001\uFF0C\u5E76\u5728\u7528\u6237\u660E\u786E\u8868\u8FBE\u610F\u56FE\u65F6\u6267\u884C\u8BBE\u5907\u63A7\u5236\u6216\u573A\u666F\u6267\u884C\u3002

\u884C\u4E3A\u89C4\u5219\uFF1A
1. \u9996\u6B21\u5DE5\u4F5C\u6216\u6536\u5230\u5237\u65B0\u8BF7\u6C42\u65F6\uFF0C\u4F18\u5148\u540C\u6B65\u8BBE\u5907\u548C\u573A\u666F\u76EE\u5F55\u3002
2. \u591A\u8DEF\u9762\u677F\u4F1A\u88AB\u5C55\u5F00\u6210\u66F4\u8D34\u8FD1\u7528\u6237\u4E60\u60EF\u7684\u5B50\u8BBE\u5907\uFF0C\u4F8B\u5982\u201C\u540A\u706F\u201D\u201C\u7B52\u706F\u201D\uFF1B\u4F18\u5148\u4F7F\u7528\u5C55\u5F00\u540E\u7684\u5B50\u8BBE\u5907\u6761\u76EE\uFF0C\u800C\u4E0D\u662F\u7236\u9762\u677F\u540D\u3002
3. \u8BBE\u5907\u540D\u79F0\u53EF\u80FD\u4E0D\u552F\u4E00\u65F6\uFF0C\u5148\u6839\u636E display_name\u3001name\u3001room_name\u3001aliases \u5339\u914D\uFF1B\u4ECD\u4E0D\u552F\u4E00\u5219\u5148\u6F84\u6E05\u3002
4. \u63A7\u5236\u8BBE\u5907\u65F6\u4F18\u5148\u4F7F\u7528 catalog_device_id\uFF0C\u4E0D\u8981\u731C\u6D4B\u8BBE\u5907 ID\u3002
5. \u706F\u5149\u4F18\u5148\u4F7F\u7528 power\u3001brightness\u3001color_temp\u3002
6. \u6E29\u63A7\u4F18\u5148\u4F7F\u7528 power\u3001temperature\u3001mode\u3001fan_speed\u3002
7. \u7A97\u5E18\u4F18\u5148\u4F7F\u7528 action\u3001position\u3002
8. \u573A\u666F\u6267\u884C\u524D\u5148\u67E5\u573A\u666F\u5217\u8868\u5E76\u786E\u8BA4 scene_id\u3002
9. \u67E5\u8BE2\u5F53\u524D\u72B6\u6001\u65F6\u4F18\u5148\u4F7F\u7528 geeklink_get_device_state\uFF1B\u5982\u9700\u770B\u6700\u8FD1\u53D8\u5316\uFF0C\u4F18\u5148\u4F7F\u7528 geeklink_get_recent_events\u3002
10. \u9664\u975E\u5F00\u53D1\u8005\u660E\u786E\u8981\u6C42\uFF0C\u4E0D\u8981\u4F7F\u7528 legacy value \u900F\u4F20\u5B57\u6BB5\u3002
11. \u8BBE\u5907\u63A7\u5236\u540E\uFF0C\u5982\u7528\u6237\u5728\u786E\u8BA4\u72B6\u6001\uFF0C\u5148\u67E5 geeklink_get_device_state\uFF1B\u5982\u4ECD\u4E0D\u786E\u5B9A\uFF0C\u518D\u8865\u5145 geeklink_get_recent_events\u3002
12. \u7F51\u5173\u8FD4\u56DE\u9519\u8BEF\u65F6\u76F4\u63A5\u8BF4\u660E\u5931\u8D25\u539F\u56E0\uFF0C\u4E0D\u8981\u7F16\u9020\u6210\u529F\u7ED3\u679C\u3002`;
var GEEKLINK_HOME_SKILL_MANIFEST = {
  name: "geeklink-home",
  version: "0.1.0",
  description: "Geeklink Home local gateway skill for device catalog, scenes, control, and state sync over LAN.",
  runtime: "nodejs",
  entry: "./dist/library.js",
  promptFile: "./skill/prompt.md",
  tools: getOpenClawToolDefinitions(),
  configSchema: {
    type: "object",
    properties: {
      gatewayHost: {
        type: "string",
        title: "Gateway Host",
        description: "Geeklink Home gateway host or base URL, for example 192.168.1.50:8080"
      },
      pairingToken: {
        type: "string",
        title: "Pairing Token",
        description: "Pairing token copied from the Geeklink app"
      },
      clientName: {
        type: "string",
        title: "Client Name",
        description: "Optional client name used during session exchange",
        default: "geeklink-openclaw-skill"
      },
      configPath: {
        type: "string",
        title: "Config Path",
        description: "Optional path used to persist session and local skill config"
      }
    },
    required: ["gatewayHost", "pairingToken"]
  }
};
function getGeeklinkHomeSkillManifest() {
  return GEEKLINK_HOME_SKILL_MANIFEST;
}
function getGeeklinkHomeSkillPrompt() {
  return GEEKLINK_HOME_SKILL_PROMPT;
}

// src/cli.ts
function addConnectionOptions(command) {
  return command.addOption(new Option("--host <host>", "gateway host or base url")).addOption(new Option("--pairing-token <token>", "gateway pairing token")).addOption(new Option("--client-name <name>", "client name used for session exchange")).addOption(new Option("--session-token <token>", "explicit session token")).addOption(new Option("--config <path>", "custom config file path"));
}
function getConnectionOptions(options) {
  return {
    host: options.host,
    pairingToken: options.pairingToken,
    clientName: options.clientName,
    sessionToken: options.sessionToken,
    configPath: options.configPath
  };
}
function resolveRuntime(options) {
  const configPath = options.configPath ?? getDefaultConfigPath();
  const current = loadConfig(configPath);
  const merged = mergeConfig(current, {
    host: options.host,
    pairingToken: options.pairingToken,
    clientName: options.clientName,
    sessionToken: options.sessionToken
  });
  if (!merged.host) {
    throw new Error("Gateway host is required. Pass --host or run login first.");
  }
  const client = new GatewayClient(merged.host, merged.sessionToken);
  return { configPath, config: merged, client };
}
async function ensureAuthorized(runtime) {
  const { configPath, config, client } = runtime;
  if (config.sessionToken && config.expiresAt && config.expiresAt > unixTimeNow() + 30) {
    client.setSessionToken(config.sessionToken);
    return runtime;
  }
  if (!config.pairingToken) {
    throw new Error("No valid session token and no pairing token available. Run login with --pairing-token.");
  }
  const clientName = config.clientName ?? "nodejs-skill";
  const auth = await client.authExchange(config.pairingToken, clientName);
  const nextConfig = {
    ...config,
    clientName: auth.client_name,
    sessionToken: auth.session_token,
    expiresAt: auth.expires_at
  };
  saveConfig(nextConfig, configPath);
  client.setSessionToken(auth.session_token);
  return {
    configPath,
    config: nextConfig,
    client
  };
}
async function refreshAuthorization(runtime) {
  const { configPath, config, client } = runtime;
  const clientName = config.clientName ?? "nodejs-skill";
  if (!config.pairingToken) {
    throw new Error("No pairing token available for session refresh.");
  }
  const auth = await client.authExchange(config.pairingToken, clientName);
  const nextConfig = {
    ...config,
    clientName: auth.client_name,
    sessionToken: auth.session_token,
    expiresAt: auth.expires_at
  };
  saveConfig(nextConfig, configPath);
  client.setSessionToken(auth.session_token);
  return {
    configPath,
    config: nextConfig,
    client
  };
}
async function runWithAuthorizationRetry(runtime, fn) {
  let resolved = await ensureAuthorized(runtime);
  try {
    return await fn(resolved);
  } catch (error) {
    if (!(error instanceof GatewayApiError) || error.status !== 401) {
      throw error;
    }
    if (!resolved.config.pairingToken) {
      throw error;
    }
    const refreshed = await refreshAuthorization({
      ...resolved,
      config: {
        ...resolved.config,
        sessionToken: void 0,
        expiresAt: void 0
      }
    });
    return fn(refreshed);
  }
}
function buildControlPayload(options) {
  const payload = {};
  if (options.power !== void 0) {
    payload.power = normalizePowerValue(String(options.power));
  }
  if (options.brightness !== void 0) {
    payload.brightness = Number(options.brightness);
  }
  if (options.colorTemp !== void 0) {
    payload.color_temp = Number(options.colorTemp);
  }
  if (options.temperature !== void 0) {
    payload.temperature = Number(options.temperature);
  }
  if (options.mode !== void 0) {
    payload.mode = String(options.mode);
  }
  if (options.fanSpeed !== void 0) {
    payload.fan_speed = String(options.fanSpeed);
  }
  if (options.action !== void 0) {
    payload.action = String(options.action);
  }
  if (options.position !== void 0) {
    payload.position = Number(options.position);
  }
  if (options.value !== void 0) {
    payload.value = String(options.value);
  }
  return payload;
}
function normalizePowerValue(input) {
  const normalized = input.trim().toLowerCase();
  if (normalized === "true" || normalized === "1") {
    return true;
  }
  if (normalized === "false" || normalized === "0") {
    return false;
  }
  return normalized;
}
function printSnapshotSummary(snapshot) {
  printJson({
    version: snapshot.version,
    device_count: snapshot.devices.length,
    devices: snapshot.devices
  });
}
function printEvents(changes) {
  printJson(changes);
}
function printEventLine(event) {
  const ts = new Date(event.ts * 1e3).toISOString();
  switch (event.type) {
    case "catalog.updated":
      process.stdout.write(`${ts} catalog.updated
`);
      return;
    case "device.state":
      process.stdout.write(`${ts} device.state ${event.device_id ?? "unknown"} ${JSON.stringify(event.state ?? event.state_raw ?? {})}
`);
      return;
    case "device.online":
      process.stdout.write(`${ts} device.online ${event.device_id ?? "unknown"} online=${String(event.online)}
`);
      return;
    case "device.removed":
      process.stdout.write(`${ts} device.removed ${event.device_id ?? "unknown"}
`);
      return;
    case "scene.executed":
      process.stdout.write(`${ts} scene.executed ${String(event.scene_id ?? "")} ${event.name ?? ""} success=${String(event.success)}
`);
      return;
  }
}
function getBooleanOption(value) {
  return value === true;
}
function createCli() {
  const program2 = new Command();
  program2.name("geeklink-home").description("CLI skill for Geeklink Home LAN gateway APIs").version("0.1.0");
  addConnectionOptions(
    program2.command("hello").description("read basic gateway hello info").action(async function action() {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      printJson(await runtime.client.hello());
    })
  );
  addConnectionOptions(
    program2.command("manifest").description("read gateway manifest").action(async function action() {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      printJson(await runtime.client.manifest());
    })
  );
  addConnectionOptions(
    program2.command("openapi").description("read gateway openapi document").action(async function action() {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      printJson(await runtime.client.openapi());
    })
  );
  addConnectionOptions(
    program2.command("login").description("exchange pairing token for session token and persist config").action(async function action() {
      const opts = this.opts();
      if (!opts.host) {
        throw new Error("login requires --host");
      }
      if (!opts.pairingToken) {
        throw new Error("login requires --pairing-token");
      }
      const runtime = resolveRuntime(getConnectionOptions(opts));
      const auth = await runtime.client.authExchange(opts.pairingToken, opts.clientName ?? "geeklink-openclaw-skill");
      const nextConfig = {
        ...runtime.config,
        host: opts.host,
        pairingToken: opts.pairingToken,
        clientName: auth.client_name,
        sessionToken: auth.session_token,
        expiresAt: auth.expires_at
      };
      saveConfig(nextConfig, runtime.configPath);
      printJson({
        ok: true,
        config_path: runtime.configPath,
        host: nextConfig.host,
        client_name: nextConfig.clientName,
        expires_at: nextConfig.expiresAt
      });
    })
  );
  addConnectionOptions(
    program2.command("logout").description("clear locally cached session token").action(async function action() {
      const opts = this.opts();
      const configPath = opts.configPath ?? getDefaultConfigPath();
      const config = loadConfig(configPath);
      saveConfig(clearSession(config), configPath);
      printJson({ ok: true, config_path: configPath, session_cleared: true });
    })
  );
  addConnectionOptions(
    program2.command("config").description("show resolved local config").action(async function action() {
      const opts = this.opts();
      const configPath = opts.configPath ?? getDefaultConfigPath();
      const config = loadConfig(configPath);
      printJson({
        config_path: configPath,
        host: config.host,
        pairingToken: config.pairingToken ? `${config.pairingToken.slice(0, 8)}...` : void 0,
        clientName: config.clientName,
        expiresAt: config.expiresAt,
        hasSessionToken: Boolean(config.sessionToken)
      });
    })
  );
  const catalog = program2.command("catalog").description("catalog commands");
  addConnectionOptions(
    catalog.command("llm").description("fetch llm-ready catalog snapshot").option("--refresh", "refresh catalog from gateway before returning", false).action(async function action() {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      const refresh = getBooleanOption(this.opts().refresh);
      const sdk = new LanLlmSkillSdk({
        host: runtime.config.host,
        pairingToken: runtime.config.pairingToken,
        clientName: runtime.config.clientName,
        sessionToken: runtime.config.sessionToken,
        configPath: runtime.configPath
      });
      printJson(await sdk.getCatalogSnapshot(refresh));
    })
  );
  addConnectionOptions(
    catalog.command("devices").description("fetch catalog devices").option("--refresh", "refresh catalog from gateway before returning", false).option("--query <text>", "optional fuzzy filter by name, room, alias or id").action(async function action() {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      const refresh = getBooleanOption(this.opts().refresh);
      const query = typeof this.opts().query === "string" ? this.opts().query.trim() : "";
      const sdk = new LanLlmSkillSdk({
        host: runtime.config.host,
        pairingToken: runtime.config.pairingToken,
        clientName: runtime.config.clientName,
        sessionToken: runtime.config.sessionToken,
        configPath: runtime.configPath
      });
      printJson({
        ok: true,
        devices: query ? await sdk.findDevicesByQuery(query, refresh) : await sdk.listDevices(refresh)
      });
    })
  );
  addConnectionOptions(
    catalog.command("scenes").description("fetch catalog scenes").option("--refresh", "refresh catalog from gateway before returning", false).action(async function action() {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      const refresh = getBooleanOption(this.opts().refresh);
      const sdk = new LanLlmSkillSdk({
        host: runtime.config.host,
        pairingToken: runtime.config.pairingToken,
        clientName: runtime.config.clientName,
        sessionToken: runtime.config.sessionToken,
        configPath: runtime.configPath
      });
      printJson({ ok: true, scenes: await sdk.listScenes(refresh) });
    })
  );
  addConnectionOptions(
    catalog.command("scene-detail").description("fetch raw catalog scene detail by scene id").argument("<sceneId>", "scene id").action(async function action(sceneId) {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      printJson(await runWithAuthorizationRetry(runtime, (resolved) => resolved.client.sceneDetail(Number(sceneId))));
    })
  );
  addConnectionOptions(
    program2.command("scene").description("scene commands").command("activate").description("activate scene by scene id").argument("<sceneId>", "scene id").action(async function action(sceneId) {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      printJson(await runWithAuthorizationRetry(runtime, (resolved) => resolved.client.activateScene(Number(sceneId))));
    })
  );
  addConnectionOptions(
    program2.command("device").description("device commands").command("control").description("control a local catalog device").argument("<deviceId>", "catalog_device_id").option("--power <value>", "power value: true/false/on/off/open/close").option("--brightness <value>", "brightness 0..100").option("--color-temp <value>", "color temperature 0..100").option("--temperature <value>", "temperature 0..31").option("--mode <value>", "mode: auto/cool/dry/fan/fan_only/heat").option("--fan-speed <value>", "fan speed: auto/low/mid/medium/high").option("--action <value>", "curtain action: open/close/stop").option("--position <value>", "curtain position 0..100").option("--value <hex>", "legacy passthrough hex value").action(async function action(deviceId) {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      const payload = buildControlPayload(this.opts());
      const sdk = new LanLlmSkillSdk({
        host: runtime.config.host,
        pairingToken: runtime.config.pairingToken,
        clientName: runtime.config.clientName,
        sessionToken: runtime.config.sessionToken,
        configPath: runtime.configPath
      });
      if (!Object.keys(payload).length) {
        throw new Error("At least one control field is required");
      }
      printJson(await sdk.controlDevice(deviceId, payload));
    })
  );
  const state = program2.command("state").description("runtime state commands");
  addConnectionOptions(
    state.command("snapshot").description("fetch runtime state snapshot").option("--refresh", "refresh snapshot from gateway before returning", false).action(async function action() {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      const refresh = getBooleanOption(this.opts().refresh);
      const sdk = new LanLlmSkillSdk({
        host: runtime.config.host,
        pairingToken: runtime.config.pairingToken,
        clientName: runtime.config.clientName,
        sessionToken: runtime.config.sessionToken,
        configPath: runtime.configPath
      });
      printSnapshotSummary(await sdk.getStateSnapshot(refresh));
    })
  );
  addConnectionOptions(
    state.command("watch").description("watch runtime state changes using long-poll").option("--since <version>", "start version", "0").option("--wait <seconds>", "long-poll wait seconds", "25").option("--json", "print full change payload as json", false).option("--with-snapshot", "print snapshot before entering long-poll", false).option("--retry-delay <ms>", "retry delay after transient errors", "2000").action(async function action() {
      let runtime = await ensureAuthorized(resolveRuntime(getConnectionOptions(this.opts())));
      let version = Number(this.opts().since ?? "0");
      const wait = Number(this.opts().wait ?? "25");
      const asJson = Boolean(this.opts().json);
      const withSnapshot = Boolean(this.opts().withSnapshot);
      const retryDelay = Number(this.opts().retryDelay ?? "2000");
      if (withSnapshot || version === 0) {
        const snapshot = await runtime.client.stateSnapshot();
        if (withSnapshot) {
          printSnapshotSummary(snapshot);
        }
        version = snapshot.version;
      }
      for (; ; ) {
        try {
          const changes = await runtime.client.stateChanges(version, wait);
          if (changes.snapshot_required) {
            const snapshot = await runtime.client.stateSnapshot();
            printJson({
              type: "snapshot.refresh",
              version_before: version,
              version_after: snapshot.version,
              device_count: snapshot.devices.length
            });
            version = snapshot.version;
            continue;
          }
          if (asJson) {
            printEvents(changes);
          } else {
            for (const event of changes.events) {
              printEventLine(event);
            }
          }
          version = Math.max(version, changes.current_version);
        } catch (error) {
          if (error instanceof GatewayApiError && error.status === 401) {
            runtime = await refreshAuthorization({
              ...runtime,
              config: {
                ...runtime.config,
                sessionToken: void 0,
                expiresAt: void 0
              }
            });
            continue;
          }
          process.stderr.write(`watch error: ${error.message}
`);
          await sleep(retryDelay);
        }
      }
    })
  );
  const openclaw = program2.command("openclaw").description("OpenClaw tool adapter helpers");
  addConnectionOptions(
    openclaw.command("tools").description("print OpenClaw-ready tool definitions").action(async function action() {
      const runtime = resolveRuntime(getConnectionOptions(this.opts()));
      const adapter = new OpenClawToolAdapter({
        host: runtime.config.host,
        pairingToken: runtime.config.pairingToken,
        clientName: runtime.config.clientName,
        sessionToken: runtime.config.sessionToken,
        configPath: runtime.configPath
      });
      printJson(adapter.getToolDefinitions());
    })
  );
  addConnectionOptions(
    openclaw.command("call").description("execute a tool through the OpenClaw adapter").argument("<toolName>", "tool name").requiredOption("--input <json>", "tool input json").action(async function action(toolName) {
      const opts = this.opts();
      const runtime = resolveRuntime(getConnectionOptions(opts));
      const adapter = new OpenClawToolAdapter({
        host: runtime.config.host,
        pairingToken: runtime.config.pairingToken,
        clientName: runtime.config.clientName,
        sessionToken: runtime.config.sessionToken,
        configPath: runtime.configPath
      });
      printJson(await adapter.executeTool(toolName, JSON.parse(opts.input)));
    })
  );
  const skill = program2.command("skill").description("standard skill package helpers");
  skill.command("manifest").description("print the standard skill manifest").action(async function action() {
    printJson(getGeeklinkHomeSkillManifest());
  });
  skill.command("prompt").description("print the standard skill system prompt").action(async function action() {
    process.stdout.write(`${getGeeklinkHomeSkillPrompt()}
`);
  });
  return program2;
}
async function runCli(argv) {
  const program2 = createCli();
  try {
    await program2.parseAsync(argv);
  } catch (error) {
    if (error instanceof GatewayApiError) {
      const detail = isObject(error.body) ? error.body : void 0;
      process.stderr.write(`Gateway error (${error.status}): ${error.message}
`);
      if (detail) {
        process.stderr.write(`${JSON.stringify(detail, null, 2)}
`);
      }
      process.exitCode = 1;
      return;
    }
    process.stderr.write(`${error.message}
`);
    process.exitCode = 1;
  }
}

// src/index.ts
void runCli(process.argv);
