/// A minimal Sui Move counter module for audit demonstration.
/// Demonstrates: object ownership, capability pattern, events.
module simple_counter::counter {
    use sui::event;

    // ======== Objects ========

    /// Admin capability — only the deployer receives this.
    public struct AdminCap has key, store {
        id: UID,
    }

    /// A shared counter object that anyone can read but only admin can reset.
    public struct Counter has key {
        id: UID,
        value: u64,
    }

    // ======== Events ========

    public struct CounterChanged has copy, drop {
        value: u64,
    }

    // ======== Init ========

    /// Module initializer: creates AdminCap for the deployer and a shared Counter.
    fun init(ctx: &mut TxContext) {
        transfer::transfer(
            AdminCap { id: object::new(ctx) },
            tx_context::sender(ctx),
        );

        transfer::share_object(
            Counter {
                id: object::new(ctx),
                value: 0,
            },
        );
    }

    // ======== Public Entry Functions ========

    /// Increment the counter by 1. Anyone can call this.
    public entry fun increment(counter: &mut Counter) {
        counter.value = counter.value + 1;
        event::emit(CounterChanged { value: counter.value });
    }

    /// Reset the counter to 0. Only admin can call this.
    public entry fun reset(_: &AdminCap, counter: &mut Counter) {
        counter.value = 0;
        event::emit(CounterChanged { value: 0 });
    }

    /// Get the current counter value.
    public fun value(counter: &Counter): u64 {
        counter.value
    }
}
