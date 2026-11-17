// The parts of the BrainChain contracts' ABIs the worker uses, from usebrainchain/brainchain release 3.1.0.

/** OpenZeppelin's ERC20 errors, which the staking and bond contracts pass through from the token. */
export const erc20Errors = [
  {
    "type": "error",
    "name": "ERC20InsufficientAllowance",
    "inputs": [
      {
        "name": "spender",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "allowance",
        "type": "uint256",
        "internalType": "uint256"
      },
      {
        "name": "needed",
        "type": "uint256",
        "internalType": "uint256"
      }
    ]
  },
  {
    "type": "error",
    "name": "ERC20InsufficientBalance",
    "inputs": [
      {
        "name": "sender",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "balance",
        "type": "uint256",
        "internalType": "uint256"
      },
      {
        "name": "needed",
        "type": "uint256",
        "internalType": "uint256"
      }
    ]
  }
] as const;

/** OpenZeppelin's errors for a token call that fails inside a contract: FailedInnerCall when it reverts with no reason, as when it runs out of gas. */
export const transferErrors = [
  {
    "type": "error",
    "name": "FailedInnerCall",
    "inputs": []
  },
  {
    "type": "error",
    "name": "SafeERC20FailedOperation",
    "inputs": [
      {
        "name": "token",
        "type": "address",
        "internalType": "address"
      }
    ]
  }
] as const;

export const taskBoardAbi = [
  {
    "type": "function",
    "name": "get",
    "inputs": [
      {
        "name": "id",
        "type": "uint256",
        "internalType": "uint256"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "tuple",
        "internalType": "struct TaskBoard.Task",
        "components": [
          {
            "name": "poster",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "bounty",
            "type": "uint128",
            "internalType": "uint128"
          },
          {
            "name": "deadline",
            "type": "uint64",
            "internalType": "uint64"
          },
          {
            "name": "status",
            "type": "uint8",
            "internalType": "enum TaskBoard.Status"
          },
          {
            "name": "accepted",
            "type": "bool",
            "internalType": "bool"
          },
          {
            "name": "disputed",
            "type": "bool",
            "internalType": "bool"
          },
          {
            "name": "disputedByModel",
            "type": "bool",
            "internalType": "bool"
          },
          {
            "name": "model",
            "type": "bytes32",
            "internalType": "bytes32"
          },
          {
            "name": "briefHash",
            "type": "bytes32",
            "internalType": "bytes32"
          },
          {
            "name": "resultHash",
            "type": "bytes32",
            "internalType": "bytes32"
          },
          {
            "name": "submittedAt",
            "type": "uint64",
            "internalType": "uint64"
          },
          {
            "name": "gradedAt",
            "type": "uint64",
            "internalType": "uint64"
          },
          {
            "name": "disputedAt",
            "type": "uint64",
            "internalType": "uint64"
          },
          {
            "name": "postedAt",
            "type": "uint64",
            "internalType": "uint64"
          },
          {
            "name": "payee",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "feeRecipient",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "feeBps",
            "type": "uint16",
            "internalType": "uint16"
          },
          {
            "name": "hireThresholdBps",
            "type": "uint16",
            "internalType": "uint16"
          },
          {
            "name": "gradeThresholdBps",
            "type": "uint16",
            "internalType": "uint16"
          },
          {
            "name": "ruleThresholdBps",
            "type": "uint16",
            "internalType": "uint16"
          },
          {
            "name": "gradeWindow",
            "type": "uint64",
            "internalType": "uint64"
          },
          {
            "name": "disputeWindow",
            "type": "uint64",
            "internalType": "uint64"
          },
          {
            "name": "ruleWindow",
            "type": "uint64",
            "internalType": "uint64"
          }
        ]
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "submit",
    "inputs": [
      {
        "name": "id",
        "type": "uint256",
        "internalType": "uint256"
      },
      {
        "name": "resultHash",
        "type": "bytes32",
        "internalType": "bytes32"
      },
      {
        "name": "resultURI",
        "type": "string",
        "internalType": "string"
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "workerAllowed",
    "inputs": [
      {
        "name": "",
        "type": "address",
        "internalType": "address"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "bool",
        "internalType": "bool"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "setWorkerAllowed",
    "inputs": [
      {
        "name": "account",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "allowed",
        "type": "bool",
        "internalType": "bool"
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "event",
    "name": "Posted",
    "inputs": [
      {
        "name": "id",
        "type": "uint256",
        "indexed": true,
        "internalType": "uint256"
      },
      {
        "name": "poster",
        "type": "address",
        "indexed": true,
        "internalType": "address"
      },
      {
        "name": "bounty",
        "type": "uint128",
        "indexed": false,
        "internalType": "uint128"
      },
      {
        "name": "deadline",
        "type": "uint64",
        "indexed": false,
        "internalType": "uint64"
      },
      {
        "name": "briefHash",
        "type": "bytes32",
        "indexed": false,
        "internalType": "bytes32"
      },
      {
        "name": "briefURI",
        "type": "string",
        "indexed": false,
        "internalType": "string"
      }
    ],
    "anonymous": false
  },
  {
    "type": "event",
    "name": "WorkerHired",
    "inputs": [
      {
        "name": "id",
        "type": "uint256",
        "indexed": true,
        "internalType": "uint256"
      },
      {
        "name": "model",
        "type": "bytes32",
        "indexed": true,
        "internalType": "bytes32"
      },
      {
        "name": "decisionId",
        "type": "uint256",
        "indexed": true,
        "internalType": "uint256"
      }
    ],
    "anonymous": false
  },
  {
    "type": "event",
    "name": "BountyPaid",
    "inputs": [
      {
        "name": "id",
        "type": "uint256",
        "indexed": true,
        "internalType": "uint256"
      },
      {
        "name": "model",
        "type": "bytes32",
        "indexed": true,
        "internalType": "bytes32"
      },
      {
        "name": "account",
        "type": "address",
        "indexed": true,
        "internalType": "address"
      },
      {
        "name": "bounty",
        "type": "uint128",
        "indexed": false,
        "internalType": "uint128"
      },
      {
        "name": "fee",
        "type": "uint128",
        "indexed": false,
        "internalType": "uint128"
      }
    ],
    "anonymous": false
  },
  {
    "type": "event",
    "name": "BountyRefunded",
    "inputs": [
      {
        "name": "id",
        "type": "uint256",
        "indexed": true,
        "internalType": "uint256"
      },
      {
        "name": "poster",
        "type": "address",
        "indexed": true,
        "internalType": "address"
      },
      {
        "name": "amount",
        "type": "uint128",
        "indexed": false,
        "internalType": "uint128"
      },
      {
        "name": "reason",
        "type": "uint8",
        "indexed": false,
        "internalType": "enum TaskBoard.RefundReason"
      }
    ],
    "anonymous": false
  },
  {
    "type": "error",
    "name": "TooLate",
    "inputs": []
  },
  {
    "type": "error",
    "name": "BadStatus",
    "inputs": []
  },
  {
    "type": "error",
    "name": "NotWorker",
    "inputs": []
  },
  {
    "type": "error",
    "name": "NotDisputant",
    "inputs": []
  }
] as const;

export const workerStakingAbi = [
  {
    "type": "function",
    "name": "stake",
    "inputs": [
      {
        "name": "amount",
        "type": "uint128",
        "internalType": "uint128"
      },
      {
        "name": "price",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "setPrice",
    "inputs": [
      {
        "name": "price",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "requestUnstake",
    "inputs": [
      {
        "name": "amount",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "withdraw",
    "inputs": [],
    "outputs": [],
    "stateMutability": "nonpayable"
  },
  {
    "type": "function",
    "name": "get",
    "inputs": [
      {
        "name": "account",
        "type": "address",
        "internalType": "address"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "tuple",
        "internalType": "struct WorkerStaking.Worker",
        "components": [
          {
            "name": "staked",
            "type": "uint128",
            "internalType": "uint128"
          },
          {
            "name": "unstaking",
            "type": "uint128",
            "internalType": "uint128"
          },
          {
            "name": "unlocksAt",
            "type": "uint64",
            "internalType": "uint64"
          },
          {
            "name": "price",
            "type": "uint128",
            "internalType": "uint128"
          },
          {
            "name": "registered",
            "type": "bool",
            "internalType": "bool"
          }
        ]
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "minStake",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "held",
    "inputs": [
      {
        "name": "",
        "type": "address",
        "internalType": "address"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "uint32",
        "internalType": "uint32"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "event",
    "name": "Slashed",
    "inputs": [
      {
        "name": "account",
        "type": "address",
        "indexed": true,
        "internalType": "address"
      },
      {
        "name": "amount",
        "type": "uint256",
        "indexed": false,
        "internalType": "uint256"
      }
    ],
    "anonymous": false
  },
  {
    "type": "error",
    "name": "BadAmount",
    "inputs": []
  },
  {
    "type": "error",
    "name": "Locked",
    "inputs": []
  },
  {
    "type": "error",
    "name": "NotHeld",
    "inputs": []
  },
  ...erc20Errors,
  ...transferErrors,
] as const;
